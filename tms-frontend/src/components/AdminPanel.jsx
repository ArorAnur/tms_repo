import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { createTask, recomputeTaskEligibility, getTasksById } from '../services/tasks'; // Import getTasksById
import AssignmentRuleBuilder from './AssignmentRuleBuilder';

function AdminPanel() {
  const { user } = useAuth();
  const [mode, setMode] = useState('CREATE'); // 'CREATE', 'REASSIGN', or 'VIEW'
  const [taskId, setTaskId] = useState('');
  const [title, setTitle] = useState('');
  const [rules, setRules] = useState([]);

  if (!user?.scopes?.includes('write')) {
    return <div>Access Denied: Requires 'write' scope.</div>;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (mode === 'CREATE') {
        const response = await createTask({ title, assignment_rules: rules });
        alert(`New task created successfully! Task Id : ${response.data.task_id}`);
      } else if (mode === 'REASSIGN') {
        if (!taskId) return alert('Task ID is required for reassignment.');
        await recomputeTaskEligibility(taskId, rules);
        alert(`Task ${taskId} eligibility recomputed successfully!`);
      } else if (mode === 'VIEW') {
        if (!taskId) return alert('Task ID is required for viewing.');
        const response = await getTasksById(taskId);
        // Displaying formatted JSON in an alert
        alert(`Task Details:\n${JSON.stringify(response, null, 2)}`);
      }
    } catch (err) {
      alert(`Operation failed: ${err.message}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ padding: '20px', maxWidth: '600px' }}>
      <h1>Task Administration</h1>

      {/* Mode Toggle */}
      <div style={{ marginBottom: '20px' }}>
        <button type="button" onClick={() => setMode('CREATE')} style={{ fontWeight: mode === 'CREATE' ? 'bold' : 'normal' }}>Create</button>
        <button type="button" onClick={() => setMode('REASSIGN')} style={{ marginLeft: '10px', fontWeight: mode === 'REASSIGN' ? 'bold' : 'normal' }}>Reassign</button>
        <button type="button" onClick={() => setMode('VIEW')} style={{ marginLeft: '10px', fontWeight: mode === 'VIEW' ? 'bold' : 'normal' }}>View</button>
      </div>

      {/* Conditional Inputs */}
      {(mode === 'REASSIGN' || mode === 'VIEW') && (
        <div style={{ marginBottom: '15px' }}>
          <input 
            value={taskId} 
            onChange={(e) => setTaskId(e.target.value)} 
            placeholder="Enter Task ID" 
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
      )}

      {mode === 'CREATE' && (
        <div style={{ marginBottom: '15px' }}>
          <input 
            value={title} 
            onChange={(e) => setTitle(e.target.value)} 
            placeholder="Task Title" 
            style={{ width: '100%', padding: '8px' }}
          />
        </div>
      )}

      {mode !== 'VIEW' && <AssignmentRuleBuilder rules={rules} setRules={setRules} />}
      
      <button 
        type="submit" 
        style={{ marginTop: '20px', padding: '10px 20px', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}
      >
        {mode === 'CREATE' ? 'Deploy Task' : mode === 'REASSIGN' ? 'Recompute Assignment' : 'Fetch Task Details'}
      </button>
    </form>
  );
}

export default AdminPanel;