from django.shortcuts import render ,redirect
from .models import Task
from django.http import HttpResponse
from .forms import SearchForm , AddTaskForm
from datetime import datetime

# Create your views here.

def tasks_list(request):
    tasks = Task.objects.all()
    completed = request.GET.get('completed')
    if completed == '1':
        tasks = tasks.filter(completed=True)
    elif completed == '0':
        tasks = tasks.filter(completed=False)
    return render(request, 'task_app/tasks_list.html', {'tasks': tasks})

def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        return render(request, 'task_app/task_detail.html', {'task': task})
    except Task.DoesNotExist:
        return HttpResponse("Task not found")

def search_task(request):
    search_form=SearchForm()
    search_task = Task.objects.all()
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_term = search_form.cleaned_data['title']
            search_task = search_task.filter(title__icontains=search_term)

    return render(request, 'task_app/search_task.html', {'search_tasks': search_task,"search_form": search_form})


def create_task(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks_list')
        else:
            return render(request, 'task_app/create_task.html', {'form': form})
    else:
        form = AddTaskForm()
        return render(request, 'task_app/create_task.html', {'form': form})

def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('tasks_list')
    except Task.DoesNotExist:
        return HttpResponse("Task not found")
    
def edit_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        if request.method == 'POST':
            form = AddTaskForm(request.POST, instance=task)
            if form.is_valid():
                task.created_at = datetime.now()
                form.save()
                return redirect('tasks_list')
            else:
                return render(request, 'task_app/edit_task.html', {'form': form})
        form = AddTaskForm(instance=task)
        return render(request, 'task_app/edit_task.html', {'form': form})
    except:
        return HttpResponse("Task not found")

