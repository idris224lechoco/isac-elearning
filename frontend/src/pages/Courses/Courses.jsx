import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNotification } from '../../contexts/NotificationContext';
import './Courses.css';

const Courses = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const { addNotification } = useNotification();

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await axios.get('/api/v1/courses/courses/');
      setCourses(response.data.results);
    } catch (error) {
      addNotification('Erreur lors du chargement des cours', 'error');
    } finally {
      setLoading(false);
    }
  };

  const enrollCourse = async (courseId) => {
    try {
      await axios.post('/api/v1/courses/enrollments/', {
        course: courseId,
      });
      addNotification('Inscription réussie!', 'success');
      fetchCourses();
    } catch (error) {
      addNotification(
        error.response?.data?.detail || 'Erreur lors de l\'inscription',
        'error'
      );
    }
  };

  if (loading) return <div className="loading">Chargement...</div>;

  return (
    <div className="courses-container">
      <h1>Cours Disponibles</h1>
      <div className="courses-grid">
        {courses.map((course) => (
          <div key={course.id} className="course-card">
            <img src={course.image || '/placeholder.jpg'} alt={course.title} />
            <div className="course-content">
              <h3>{course.title}</h3>
              <p className="description">{course.description}</p>
              <div className="course-info">
                <span className="price">{course.price} {course.currency}</span>
                <span className="level">{course.level}</span>
              </div>
              <button
                onClick={() => enrollCourse(course.id)}
                className="enroll-btn"
              >
                S'inscrire
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Courses;
