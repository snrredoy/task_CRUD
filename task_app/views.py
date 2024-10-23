from django.shortcuts import render ,redirect
from .models import Task
from django.http import HttpResponse
from .forms import SearchForm , AddTaskForm
from datetime import datetime

from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def tasks_list(request):
    tasks = Task.objects.filter(user=request.user)
    completed = request.GET.get('completed')
    if completed == '1':
        tasks = tasks.filter(completed=True)
    elif completed == '0':
        tasks = tasks.filter(completed=False)
    return render(request, 'task_app/tasks_list.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        return render(request, 'task_app/task_detail.html', {'task': task})
    except Task.DoesNotExist:
        return HttpResponse("Task not found")

@login_required
def search_task(request):
    search_task = Task.objects.filter(user=request.user)
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_term = search_form.cleaned_data['title']
            search_task = search_task.filter(title__icontains=search_term)
    else:
        search_form = SearchForm()

    return render(request, 'task_app/search_task.html', {'search_tasks': search_task,"search_form": search_form})


@login_required
def create_task(request):
    if request.method == 'POST':
        form = AddTaskForm(request.POST)
        if form.is_valid():
            task=form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks_list')
        else:
            return render(request, 'task_app/create_task.html', {'form': form})
    else:
        form = AddTaskForm()
        return render(request, 'task_app/create_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        return redirect('tasks_list')
    except Task.DoesNotExist:
        return HttpResponse("Task not found")
    
@login_required
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

def home_view(request):
    return render(request, 'task_app/home.html')