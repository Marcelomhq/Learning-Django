from django.shortcuts import render, redirect,get_object_or_404
from .models import Task, User, RegKey
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password


# Create your views here.


class TaskListView(generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        return Task.objects.all()

class CreateView(generic.CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks:task_list')

class TaskUpdateView(generic.UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks:task_list')

class TheLoginView(LoginView):
    template_name = 'tasks/login_screen.html'
    # success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        messages.success(self.request,"You have succesfully logged in!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('tasks:task_list')  
    
class RegisterView(FormView):
    template_name = "tasks/register_screen.html"
    form_class = RegisterForm
    success_url = reverse_lazy("tasks:login")

    def form_valid(self,form):
        username = form.cleaned_data['username']
        password = form.clean_password()
        reg_key = form.cleaned_data['reg_key']

        reg_key_obj = RegKey.objects.get(reg_key=reg_key)
        
        User.objects.create(username=username, password = password, reg_key = reg_key_obj)

        messages.success(self.request, "Registration Successfull, log in now!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")
        return super().form_invalid(form)
        
            


def TaskDirectDeleteView(request, task_id):
    task = get_object_or_404(Task, id = task_id)
    task.delete()
    return redirect('tasks:task_list')

class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

# def task_list(request):
#     tasks = Task.objects.all()
#     return render(request, 'tasks/task_list.html',{'tasks':tasks})


# def task_create(request):
#     if request.method =="POST":
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         Task.objects.create(title=title, description = description)
#         return redirect('task_list')
#     return render(request,'tasks/task_form.html')

# def task_update(request, task_id):
#     task = get_object_or_404(Task, id = task_id)
#     if request.method == "POST":
#         task.title = request.POST.get('title')
#         task.description = request.POST.get('description')
#         task.completed = 'completed' in request.POST
#         task.save()
#         return redirect('task_list')
#     return render(request,'tasks/task_form.html',{'task':task})

