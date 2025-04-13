from django.urls import path
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from . import views
app_name = "tasks"



urlpatterns = [
    path("",RedirectView.as_view(pattern_name="tasks:authenticate",permanent="False")),
    path("authenticate/", views.AuthenticationView.as_view(), name="authenticate"),
    # path("resetpass/", views.ResetPasswordView.as_view(), name="resetpass"),

    path("task_list/", views.TaskListView.as_view(), name='task_list'),
    path("create/", views.CreateView.as_view(), name='task_create'),
    path("update/<int:pk>/", views.TaskUpdateView.as_view(), name="task_update"),
    path("delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),  
]