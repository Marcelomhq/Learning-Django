from django.shortcuts import render, redirect,get_object_or_404
from .models import Task, User, RegKey
from django.views import generic,View
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
from django.http import JsonResponse
from datetime import date
from calendar import monthrange,monthcalendar
from collections import defaultdict
from django.views.generic import TemplateView



# Create your views here.

class BaseLoginRequiredView(LoginRequiredMixin):
    login_url = reverse_lazy("tasks:authenticate")
    redirect_field_name = None

#New Task list, testing, maybe definitive 22/04/25
def get_monthly_tasks(user,year,month):
    start = date(year, month, 1)
    end = date(year,month,monthrange(year,month)[1])

    tasks = Task.objects.filter(
        user_tag = user,
        date__range=(start,end)
    )

    calendar_data = defaultdict(list)
    for task in tasks:
        calendar_data[task.date.day].append(task)
    
    return calendar_data

class TaskCalendarView(BaseLoginRequiredView,TemplateView):
    template_name = "calendar/teste.html"

    def get_context_data(self, **kwargs):
        from datetime import datetime
        context = super().get_context_date(**kwargs)
        year = int(self.request.GET.get("year",datetime.now().year))
        month = int(self.request.GET.get("month",datetime.now().month))

        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1

        weeks = monthcalendar(year,month)
        tasks_by_day = get_monthly_tasks(self.request.user,year,month)

        context.update({
            "weeks": weeks,
            "tasks_by_day": tasks_by_day,
            "month": month,
            "year": year,
        })
        return context

#Old Task list views.
class TaskListView(BaseLoginRequiredView,generic.ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    # login_url = "/login/"
    # redirect_field_name = None


    def get_queryset(self):
        return Task.objects.filter(user_tag = self.request.user).order_by('-created_at')
    

class CreateView(BaseLoginRequiredView,generic.CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['title', 'description']

    def form_valid(self,form):
        form.instance.user_tag = self.request.user
        return super().form_valid(form)
    
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
        # messages.success(request, "You've been logged out successfully!")
        return redirect(reverse_lazy("tasks:authenticate"))

#DISABLED FOR NOW EVERYTHING GOES THROUGH AuthenticateView
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
     
#DISABLED FOR NOW EVERYTHING GOES THROUGH AuthenticateView    
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



class AuthenticationView(View):

    template_name = 'tasks/login_screen.html' # Single template
    login_form_class = TheLoginForm
    register_form_class = RegisterForm
    login_success_url = reverse_lazy('tasks:task_list')

    #disabling this for now
    # register_success_url = reverse_lazy('tasks:authenticate')
   
    
    def get(self, request, *args, **kwargs):
        # Display both forms empty on GET request
        login_form = self.login_form_class()
        register_form = self.register_form_class()
        context = {
            'login_form': login_form,
            'register_form': register_form,
            #Disabling this for now, trying a differente approach
            # 'show_register': False
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form_type = 'unknown'
        
        if 'login_submit' in request.POST:
            form_type = 'login'
            form = self.login_form_class(request.POST)
        elif 'register_submit' in request.POST:
            form_type = 'register'
            form = self.register_form_class(request.POST)
        else:
            return JsonResponse({'status': 'error', 'errors': {'__all__': ['Form type unknown.']}}, status=400)
        
        if form.is_valid():
            if form_type == 'login':
                user = form.cleaned_data["user"]
                login(request, user)
                # Return success and redirect URL for login
                return JsonResponse({
                    'status': 'success',
                    'redirect_url': self.login_success_url
                })
            elif form_type == 'register':
                # Registration logic
                username = form.cleaned_data.get("username").lower()
                password = form.cleaned_data.get("password")
                reg_key_obj = form.cleaned_data.get("reg_key_obj")
                first_name = form.cleaned_data.get("first_name") # Get first/last names
                last_name = form.cleaned_data.get("last_name")

                user = User.objects.create_user( # Store the created user
                    username=username,
                    email=username,
                    password=password,
                    reg_key=reg_key_obj,
                    first_name=first_name,
                    last_name=last_name
                )
                reg_key_obj.used = True
                reg_key_obj.save()

                # Return success and a message for registration
                return JsonResponse({
                    'status': 'success',
                    'message': 'Registration Successful! Please log in.'
                })
        else:
            # Form is invalid, return errors as JSON
            # form.errors.get_json_data() provides a serializable dict
            return JsonResponse({
                'status': 'error',
                'form_type': form_type, # Send back which form had errors
                'errors': form.errors.get_json_data()
            }, status=400) # Use 400 status code for bad request/validation error

        # login_form = self.login_form_class()
        # register_form = self.register_form_class()
        # context = {
        #     'login_form': login_form,
        #     'register_form': register_form,
        #     'show_register': False # Default to false for POST too
        # }

        # Check which form was submitted based on the submit button's name
        # if 'login_submit' in request.POST:
        #     login_form = self.login_form_class(request.POST)
        #     if login_form.is_valid():
        #         user = login_form.cleaned_data["user"]
        #         login(request, user)
        #         # Clear existing messages before adding a new one
        #         list(get_messages(request))
        #         messages.success(request, "Login successful!")
        #         return redirect(self.login_success_url)
        #     # If login form is invalid, fall through to render both forms again
        #     # The invalid login_form (with errors) will be used in the context
        
        # elif 'register_submit' in request.POST:
        #     register_form = self.register_form_class(request.POST)
        #     if register_form.is_valid():
        #         # Registration logic from your old RegisterView.form_valid
        #         first_name = register_form.cleaned_data.get("first_name")
        #         last_name = register_form.cleaned_data.get("last_name")
        #         username = register_form.cleaned_data.get("username").lower()
        #         password = register_form.cleaned_data.get("password")
        #         reg_key_obj = register_form.cleaned_data.get("reg_key_obj") # Get from cleaned_data

        #         User.objects.create_user(
        #             username=username,
        #             email=username,                    
        #             password=password,
        #             reg_key=reg_key_obj,
        #             first_name=first_name,
        #             last_name=last_name
        #         )
        #         reg_key_obj.used = True
        #         reg_key_obj.save()

        #         # Clear existing messages before adding a new one
        #         list(get_messages(request))
        #         messages.success(request, "Registration Successful! Please log in.")
        #         context['show_register'] = False
        #         return redirect(self.register_success_url)
        #     else:
        #         context['show_register'] = True

        # return render(request, self.template_name, context)
        # If neither form was valid or properly submitted, render template with both forms
        # context = {
        #     'login_form': login_form,       # Will contain errors if login failed validation
        #     'register_form': register_form, # Will contain errors if register failed validation
        # }
        

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

