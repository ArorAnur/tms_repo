import api from './api';

/**
 * Fetch a paginated chunk of tasks assigned to the current staff user.
 */
export const getMyAssignedTasks = async (limit = 10, offset = 0) => {
  const response = await api.get(`/my-eligible-tasks/?limit=${limit}&offset=${offset}`);
  return response.data; // Return the parsed body payload natively
};


export const getTasksById = async (taskId) => {
  const response = await api.get(`/tasks/${taskId}/`);
  return response.data; // Return the parsed body payload natively
};

/**
 * Submit an administrative payload to re-evaluate structural matching workflows.
 */
export const recomputeTaskEligibility = async (taskId, assignmentRules) => {
  const response = await api.post(`/tasks/${taskId}/recompute-eligibility/`, {
    assignment_rules: assignmentRules
  });
  return response.data;
};



export const createTask = async (taskData) => {
  return await api.post('api/tasks/create/', taskData);
};

// Recompute endpoint (Assuming it follows a similar pattern)
export const recomputeTaskAssignment = async (taskId, rules) => {
  return await api.post(`/tasks/${taskId}/recompute/`, { assignment_rules: rules });
};

export const markTaskCompleted = async (taskId) => {
  return await api.put(`/tasks/${taskId}/mark-completed/`);
}