from django.shortcuts import render, redirect, get_list_or_404,get_object_or_404
from .models import Task
from django.views import generic
from django.urls import reverse_lazy

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

