from .auth_views import MyTokenObtainPairView
from .auth_views import MyTokenRefreshView
from .dashboard_views import DashboardDataView
from .task_views import CreateTaskView
from .user_views import RegisterUserView
from .task_views import MyEligibleTasksView
from .task_views import RecomputeEligibilityView
from .task_views import MarkTaskCompletedView

__all__ = [
    'MyTokenObtainPairView',
    'DashboardDataView',
    'CreateTaskView',
    'RegisterUserView',
    'MyEligibleTasksView',
    'RecomputeEligibilityView',
    'MarkTaskCompletedView',
]