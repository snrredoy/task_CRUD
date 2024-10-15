from django.urls import path

from . import views

urlpatterns =[
    path('', views.tasks_list , name='tasks_list'),
    path('tasks_list/', views.tasks_list , name='tasks_list'),
    path('<int:task_id>', views.task_detail, name= 'task_detail'),
    path('search_task/', views.search_task, name= 'search_task'),
    path('create_task/', views.create_task, name='create_task'),
    path('delete_task/<int:task_id>', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>', views.edit_task, name='edit_task'),
]