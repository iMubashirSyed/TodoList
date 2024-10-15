from django.urls import path
from . import views
# . means that we are importing from the same folder

urlpatterns = [
    path('', views.home,name="home"),
    path('edit/<int:todo_id>', views.edit_task,name="edit_task"),
    path('register', views.register,name="register"),
    path('todo/', views.todoList,name="todo_list"),
    path('logout', views.logout_page,name="logout"),
    path('login',views.login_page,name='login'),
    path('create', views.create_todo,name="create_todo"),
    path('complete/<int:todo_id>', views.complete_todo,name="complete_todo"),
    path('delete/<int:todo_id>', views.delete_todo,name="delete_todo"),
    path('get_title/', views.get_title,name="get_title"),
    path('upload_form',views.upload_form,name="upload_form"),
]