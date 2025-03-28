from django.urls import path
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from . import views
app_name = "tasks"

# def redirect_to_login(request):
#     return redirect("tasks:login")

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="tasks:login", permanent="False")),
    path("login/", views.TheLoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),

    path("task_list/", views.TaskListView.as_view(), name='task_list'),
    path("create/", views.CreateView.as_view(), name='task_create'),
    path("update/<int:pk>/", views.TaskUpdateView.as_view(), name="task_update"),
    path("delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),  
]