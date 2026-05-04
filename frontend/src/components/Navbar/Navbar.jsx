import React from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">
          <h2>ISAC E-Learning</h2>
        </div>
        <ul className="nav-menu">
          <li className="nav-item">
            <a href="/" className="nav-link">Accueil</a>
          </li>
          <li className="nav-item">
            <a href="/courses" className="nav-link">Cours</a>
          </li>
          <li className="nav-item dropdown">
            <a href="#" className="nav-link">{user?.full_name}</a>
            <div className="dropdown-menu">
              <a href="/profile" className="dropdown-item">Profil</a>
              <a href="/settings" className="dropdown-item">Paramètres</a>
              <hr />
              <button onClick={handleLogout} className="dropdown-item logout">Déconnexion</button>
            </div>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
