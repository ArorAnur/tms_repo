"""
URL configuration for TMS_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from TMS_system.views.auth_views import MyTokenObtainPairView
from TMS_system.views.auth_views import MyTokenRefreshView
from TMS_system.views.task_views import CreateTaskView
from TMS_system.views import DashboardDataView
from TMS_system.views.user_views import RegisterUserView
from TMS_system.views.task_views import MyEligibleTasksView
from TMS_system.views.task_views import RecomputeEligibilityView
from TMS_system.views.task_views import MarkTaskCompletedView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', DashboardDataView.as_view(), name='dashboard_data'),
    path('api/tasks/create/', CreateTaskView.as_view(), name='create_task'),
    path('auth/register/', RegisterUserView.as_view(), name='user-register'),
    path('my-eligible-tasks/', MyEligibleTasksView.as_view(), name='my-eligible-tasks'),
    path('tasks/<int:task_id>/recompute-eligibility/', RecomputeEligibilityView.as_view(), name='recompute-eligibility'),
    path('tasks/<int:task_id>/mark-completed/', MarkTaskCompletedView.as_view(), name='mark-task-completed'),
]
