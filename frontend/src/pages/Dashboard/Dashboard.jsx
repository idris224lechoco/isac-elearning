import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard">
      <div className="welcome-section">
        <h1>Bienvenue, {user?.full_name}!</h1>
        <p>Connecté en tant que {user?.role}</p>
      </div>

      <div className="dashboard-grid">
        {user?.role === 'student' && (
          <>
            <div className="dashboard-card">
              <h3>Mes Cours</h3>
              <p>Accédez à vos cours inscrits</p>
              <a href="/courses">Voir les cours</a>
            </div>
            <div className="dashboard-card">
              <h3>Mes Évaluations</h3>
              <p>Consultez vos notes et évaluations</p>
              <a href="/grades">Voir les notes</a>
            </div>
            <div className="dashboard-card">
              <h3>Mes Certificats</h3>
              <p>Téléchargez vos certificats</p>
              <a href="/certificates">Voir les certificats</a>
            </div>
          </>
        )}

        {user?.role === 'teacher' && (
          <>
            <div className="dashboard-card">
              <h3>Mes Cours</h3>
              <p>Gérez vos cours</p>
              <a href="/teacher/courses">Gérer les cours</a>
            </div>
            <div className="dashboard-card">
              <h3>Évaluations</h3>
              <p>Créez et gérez les quiz</p>
              <a href="/teacher/assessments">Gérer les quiz</a>
            </div>
            <div className="dashboard-card">
              <h3>Rapports</h3>
              <p>Consultez les rapports d'apprentissage</p>
              <a href="/teacher/reports">Voir les rapports</a>
            </div>
          </>
        )}

        {user?.role === 'admin' && (
          <>
            <div className="dashboard-card">
              <h3>Utilisateurs</h3>
              <p>Gérez les utilisateurs</p>
              <a href="/admin/users">Gérer les utilisateurs</a>
            </div>
            <div className="dashboard-card">
              <h3>Cours</h3>
              <p>Gérez tous les cours</p>
              <a href="/admin/courses">Gérer les cours</a>
            </div>
            <div className="dashboard-card">
              <h3>Paiements</h3>
              <p>Gérez les paiements</p>
              <a href="/admin/payments">Gérer les paiements</a>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
