from django.shortcuts import render, redirect,get_object_or_404
from .models import Task, User, RegKey
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic.edit import FormView
from .forms import RegisterForm,TheLoginForm
from django.contrib.auth.hashers import make_password
from django.contrib.messages import get_messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings



# Create your views here.

class BaseLoginRequiredView(LoginRequiredMixin):
    login_url = reverse_lazy("tasks:login")
    redirect_field_name = None

class TaskListView(BaseLoginRequiredView,generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    # login_url = "/login/"
    # redirect_field_name = None


    def get_queryset(self):
        return Task.objects.all()
    

class CreateView(BaseLoginRequiredView,generic.CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('tasks:task_list')
    # login_url = "/login/"
    # redirect_field_name = None

class TaskUpdateView(BaseLoginRequiredView,generic.UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks:task_list')
    # login_url = "/login/"
    # redirect_field_name = None

class TaskDeleteView(BaseLoginRequiredView,generic.DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

    # login_url = "/login/"
    # redirect_field_name = None

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You've been logged out successfully!")
        return redirect(reverse_lazy("tasks:login"))

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
        username = form.cleaned_data.get("username").lower()
        password = form.cleaned_data.get("password")
        reg_key = form.cleaned_data.get("reg_key_obj")
        
        reg_key_obj = RegKey.objects.get(reg_key=reg_key)    
        # User.objects.create(username=username, password = password, reg_key= reg_key_obj)
        User.objects.create_user(
            username=username,
            email=username,
            password=password,
            reg_key = reg_key_obj)       

        reg_key_obj.used = True
        reg_key_obj.save()
        # User.objects.create(username=username, password=make_password(password), reg_key=reg_key_obj)
        # RegKey.objects.filter(reg_key=reg_key).update(used=True)
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
        
            

# @method_decorator(login_required, name='dispatch')
# def TaskDirectDeleteView(request, task_id):
#     task = get_object_or_404(Task, id = task_id)
#     task.delete()
#     return redirect('tasks:task_list')




#Will leave this here in case i want to avoid redundancy
# def require_login(get_response):

#     def middleware(request):
#         allowed_paths = [settings.LOGIN_URL,"/register/"]

#         if not request.user.is_authenticated and request.path not in allowed_paths:
#             return redirect(settings.LOGIN_URL)
#         return get_response(request)
    
#     return middleware

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

