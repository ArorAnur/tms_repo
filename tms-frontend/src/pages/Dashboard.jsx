import React, { useState, useEffect } from 'react';
import TaskCard from '../components/TaskCard';
import PaginationBar from '../components/PaginationBar';
import { getMyAssignedTasks } from '../services/tasks';
import WelcomeBanner from '../components/WelcomeBanner';
import AdminPanel from '../components/AdminPanel';
import { markTaskCompleted } from '../services/tasks';
function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [offset, setOffset] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const limit = 5;


  


  const handleMarkCompleted = async (taskId) => {
    try {
      const response = await markTaskCompleted(taskId);
      console.log("Mark completed response:", response);
      if(response.status === 200) {

        // Update the local state to reflect the change immediately
        setTasks(tasks => tasks.map(task => 
          task.task_id === taskId ? { ...task, status: 'COMPLETED' } : task
        ));
      } 
      // Optionally, refetch tasks or update state to reflect the change
      
    } catch (error) {
      console.error("Failed to mark task as completed:", error);
    }
  };

  

    // You would call an API endpoint here to update the task status
  


  useEffect(() => {
    const fetchTasks = async () => {
      setIsLoading(true);
      try {
        const data = await getMyAssignedTasks(limit, offset);
        
        // Adjust these keys if your API wraps the payload differently 
        // e.g., data.results, data.items, data.count
        setTasks(data.results || []); 
        setTotalCount(data.results.length || 0);
      } catch (error) {
        console.error("Failed to fetch assigned tasks:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTasks();
  }, [offset]); // Triggers re-fetch automatically whenever the user changes pages

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
     <WelcomeBanner />
      <h2>My Assigned Tasks</h2>
      
      {/* Loading Skeleton / Spinner State */}
      {isLoading ? (
        <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
          Loading active fleet tasks...
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {tasks.map(task => (
            <TaskCard key={task.task_id} task={task} markCompletedHandler={() => handleMarkCompleted(task.task_id)} />
          ))}
          {tasks.length === 0 && (
            <p style={{ textAlign: 'center', color: '#888' }}>No tasks assigned.</p>
          )}
        </div>
      )}

      {/* Control Layer tied to Server Metrics */}
      <PaginationBar 
        offset={offset}
        limit={limit}
        totalCount={totalCount}
        onPrevious={() => setOffset(prev => Math.max(0, prev - limit))}
        onNext={() => setOffset(prev => {
          // Guard against over-advancing past server-reported boundaries
          return prev + limit < totalCount ? prev + limit : prev;
        })}
        isLoading={isLoading}
      />

      <AdminPanel />
    </div>
  );
}

export default Dashboard;