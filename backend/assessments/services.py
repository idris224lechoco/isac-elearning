from django.utils import timezone
from decimal import Decimal
from .models import QuizAttempt, Answer, Grade
from courses.models import Enrollment

class QuizEvaluationService:
    """Service pour évaluer les quiz"""
    
    @staticmethod
    def evaluate_quiz_attempt(attempt: QuizAttempt) -> dict:
        """Évaluer une tentative de quiz"""
        attempt.submitted_at = timezone.now()
        
        total_points = 0
        earned_points = Decimal('0')
        
        # Calculer les points
        answers = attempt.answers.all()
        for answer in answers:
            total_points += answer.question.points
            
            if answer.question.question_type == 'mcq':
                if answer.selected_choice and answer.selected_choice.is_correct:
                    answer.is_correct = True
                    answer.points_earned = Decimal(answer.question.points)
                    earned_points += answer.points_earned
                else:
                    answer.is_correct = False
            
            answer.save()
        
        # Calculer le pourcentage
        if total_points > 0:
            percentage = (earned_points / Decimal(total_points)) * 100
        else:
            percentage = 0
        
        attempt.score = earned_points
        attempt.percentage = int(percentage)
        attempt.is_passed = percentage >= attempt.quiz.passing_percentage
        attempt.save()
        
        # Créer la note si c'est la dernière tentative
        if attempt.attempt_number == attempt.quiz.attempts_allowed or attempt.is_passed:
            QuizEvaluationService.create_or_update_grade(
                attempt.student,
                attempt.quiz.course
            )
        
        return {
            'score': float(earned_points),
            'percentage': attempt.percentage,
            'is_passed': attempt.is_passed,
            'total_points': total_points
        }
    
    @staticmethod
    def create_or_update_grade(student, course) -> Grade:
        """Créer ou mettre à jour la note d'un étudiant pour un cours"""
        # Calculer la note moyenne
        attempts = QuizAttempt.objects.filter(
            student=student,
            quiz__course=course,
            submitted_at__isnull=False
        ).order_by('-submitted_at')
        
        if not attempts.exists():
            return None
        
        # Moyenne des meilleures tentatives
        best_score = attempts.first().percentage
        
        # Déterminer la lettre de grade
        if best_score >= 90:
            grade_letter = 'A'
        elif best_score >= 80:
            grade_letter = 'B'
        elif best_score >= 70:
            grade_letter = 'C'
        elif best_score >= 60:
            grade_letter = 'D'
        else:
            grade_letter = 'F'
        
        grade, created = Grade.objects.update_or_create(
            student=student,
            course=course,
            defaults={
                'total_score': best_score,
                'grade_letter': grade_letter
            }
        )
        
        return grade


class CertificateService:
    """Service pour générer les certificats"""
    
    @staticmethod
    def generate_certificate_number() -> str:
        """Générer un numéro de certificat unique"""
        from django.utils import timezone
        import uuid
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"CERT-{timestamp}-{unique_id}"
    
    @staticmethod
    def can_issue_certificate(student, course) -> bool:
        """Vérifier si un certificat peut être émis"""
        try:
            # Vérifier l'inscription
            from courses.models import Enrollment
            enrollment = Enrollment.objects.get(student=student, course=course)
            
            # Vérifier la grade
            grade = Grade.objects.get(student=student, course=course)
            
            # Doit avoir au moins une C (70%)
            return grade.grade_letter in ['A', 'B', 'C']
        except (Enrollment.DoesNotExist, Grade.DoesNotExist):
            return False


class PaymentService:
    """Service pour gérer les paiements"""
    
    @staticmethod
    def process_payment(payment) -> dict:
        """Traiter un paiement"""
        from .models import PaymentLog
        
        try:
            # Vérifier le statut actuel
            if payment.status not in ['pending', 'processing']:
                raise ValueError(f"Ne peut pas traiter un paiement avec le statut: {payment.status}")
            
            # Créer le log
            PaymentLog.objects.create(
                payment=payment,
                status_before=payment.status,
                status_after='completed',
                message='Paiement traité avec succès',
                response_data={}
            )
            
            # Mettre à jour le paiement
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()
            
            # Créer l'inscription
            from courses.models import Enrollment
            enrollment, created = Enrollment.objects.get_or_create(
                student=payment.student,
                course=payment.course,
                defaults={
                    'status': 'active',
                    'enrollment_date': timezone.now()
                }
            )
            
            return {
                'success': True,
                'message': 'Paiement traité avec succès',
                'payment_id': str(payment.id)
            }
        
        except Exception as e:
            # Créer le log d'erreur
            from .models import PaymentLog
            PaymentLog.objects.create(
                payment=payment,
                status_before=payment.status,
                status_after='failed',
                message=f'Erreur de paiement: {str(e)}',
                response_data={'error': str(e)}
            )
            
            payment.status = 'failed'
            payment.save()
            
            return {
                'success': False,
                'message': str(e),
                'payment_id': str(payment.id)
            }
