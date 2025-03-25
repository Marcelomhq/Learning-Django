from django.shortcuts import render, redirect,get_object_or_404
from .models import Task, User, RegKey
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from .forms import RegisterForm,TheLoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.messages import get_messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.


class TaskListView(LoginRequiredMixin,generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    login_url = "/login/"

    def get_queryset(self):
        return Task.objects.all()
    

class CreateView(LoginRequiredMixin,generic.CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks:task_list')
    login_url = "/login/"

class TaskUpdateView(generic.UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks:task_list')

class TheLoginView(FormView):
    template_name = 'tasks/login_screen.html'
    form_class = TheLoginForm
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):

        user = form.cleaned_data["user"]

        # username = form.cleaned_data["username"]
        # password = form.cleaned_data["password"]
        
        # # user = User.objects.get(username=username)
        # user = authenticate(username=username, password=password)

        login(self.request,user)          

        
        storage = get_messages(self.request)
        list(storage)

        messages.success(self.request, "Login succesful!")
        return super().form_valid(form)
    
    # def form_invalid(self, form):
    #     for field, errors in form.errors.items():
    #         for error in errors:
    #             messages.error(self.request, f"{field}: {error}")
    #     return super().form_invalid(form)
    # def form_invalid(self, form):
    #     messages.error(self.request, 'Invalid username or password. Please try again.')
    #     return super().form_invalid(form)
     
    
class RegisterView(FormView):
    template_name = "tasks/register_screen.html"
    form_class = RegisterForm
    success_url = reverse_lazy("tasks:login")

    def form_valid(self,form):
        username = form.clean_username()
        password = form.clean_password()
        reg_key = form.clean_reg_key()
        
        reg_key_obj = RegKey.objects.get(reg_key=reg_key)    
        # User.objects.create(username=username, password = password, reg_key= reg_key_obj)
        User.objects.create(username=username, password=make_password(password), reg_key=reg_key_obj)
        RegKey.objects.filter(reg_key=reg_key).update(used=True)
        # form.username.errors,form.password.errors,form.reg_key.errors = None
        
        storage = get_messages(self.request)
        list(storage)

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

