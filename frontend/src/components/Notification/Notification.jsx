import React from 'react';
import { useNotification } from '../contexts/NotificationContext';
import './Notification.css';

const Notification = () => {
  const { notifications, removeNotification } = useNotification();

  return (
    <div className="notification-container">
      {notifications.map((notif) => (
        <div key={notif.id} className={`notification notification-${notif.type}`}>
          <p>{notif.message}</p>
          <button onClick={() => removeNotification(notif.id)}>×</button>
        </div>
      ))}
    </div>
  );
};

export default Notification;
