from django.urls import path
from . import views
app_name = "tasks"
urlpatterns = [
    path("task_list", views.TaskListView.as_view(), name='task_list'),
    path("create/", views.CreateView.as_view(), name='task_create'),
    path("update/<int:pk>/", views.TaskUpdateView.as_view(), name="task_update"),
    path("delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("login/", views.TheLoginView.as_view(), name="login"),
    path("", views.TheLoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register")

]