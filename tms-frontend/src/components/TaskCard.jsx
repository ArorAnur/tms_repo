import React, { useEffect } from 'react';

export default function TaskCard({ task, markCompletedHandler }) {


 
  // Helper to change color based on status
  const getStatusColor = (status) => {
    if (status.toLocaleLowerCase() === 'completed') return 'green';
    if (status.toLocaleLowerCase() === 'unassigned') return 'orange';
    return 'blue';
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '4px', backgroundColor: '#fff' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <strong style={{ fontSize: '16px' }}>{task.title}</strong>
        <small style={{ color: getStatusColor(task.status), fontWeight: 'bold' }}>
          {task.status}
        </small>
        <button style={{ padding: '6px 12px', backgroundColor: '#007bff', color: '#fff', border: 'none', borderRadius: '4px', cursor: 'pointer' }} onClick={() => markCompletedHandler(task.task_id)}>Mark Completed</button>
      </div>
      <p style={{ margin: '8px 0 0 0', color: '#555', fontSize: '14px', lineHeight: '1.4' }}>
        {task.description}
    </p>
    </div>
  );
}