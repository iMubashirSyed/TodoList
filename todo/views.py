from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task, Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from datetime import datetime, timedelta
from .tasks import send_task_reminder
import csv
import io

@login_required(login_url='login')
def todoList(request):
    # returns the tasks of the current user
    todos = Task.objects.filter(user=request.user)
    
    selected_category = request.GET.get('category')
    # title_search = request.GET.get('title')
    
    # if title_search:
    #     todos = todos.filter(title__icontains=title_search)
    
    if selected_category:
        todos = todos.filter(category__name=selected_category)
    
    sort_by = request.GET.get('sort_by')
    # search = request.GET.get('search')
    # print(f'search {search}')
    # if search:
    #     todos = todos.filter(title__startswith=search)
    #     print(f'todos {todos}')
    
    # CSV file input code
    if request.method == 'POST':
        file = request.FILES['file']        
    
        decoded_file = io.TextIOWrapper(file.file, encoding="utf-8")
        reader = csv.reader(decoded_file, delimiter=",")
        # print(reader)
        
        for row in reader:
            title = row[0]        
            description = row[1]
            due_date = row[2]
            priority = row[3]
            category = row[4]
            category = Category.objects.create(name=category)
            due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
            Task.objects.create(user=request.user, title=title, desciption = description, priority=priority, due_date=due_date, category=category)
        
        return redirect('todo_list')

    search_query = request.GET.get('search', '')
    if search_query:
        # Filter tasks based on the search query
        todos = todos.filter(title__startswith=search_query)
        
    if request.headers.get('HX-Request') == 'true':
        # Return only the partial template
        return render(request, 'todo_list.html', {'todos': todos})
    
    if sort_by == 'due_date_desc':
        todos = todos.order_by('-due_date')
    elif sort_by == 'due_date_asc':
        todos = todos.order_by('due_date')
    elif sort_by == 'priority_asc':
        todos = todos.order_by('priority')
    elif sort_by == 'priority_desc':
        todos = todos.order_by('-priority')
    
    # for task in todos:
        # reminder_time = task.due_date - timedelta(days=1)
        # send_task_reminder.apply_async((task.id,), eta=reminder_time)

    return render(request, 'index.html', {'todos': todos, 'search_query': search_query})
    
@login_required(login_url='login')
def create_todo(request):
    # All the method are POST because the action type of form is POST, Hence it should be same. 
    if request.method == 'POST':
        description = request.POST.get('description')
        title = request.POST.get('title')
        priority = request.POST.get('priority') or 1
        due_date = request.POST.get('due_date')
        category = request.POST.get('category')
        category = Category.objects.create(name=category)
        task = Task.objects.create(user=request.user, title=title, desciption=description, priority=priority, due_date=due_date, category=category)
        
        send_task_reminder.delay(task.id)

    return redirect('todo_list')

# def upload_form(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
        
#         decoded_file = file.read().decode('utf-8')
#         reader = csv.reader(file, delimiter=",")
#         # print(reader)
        
#         for row in reader:
#             title = row[0]        
#             description = row[1]
#             due_date = row[2]
#             priority = row[3]
#             category = row[4]
#             category = Category.objects.create(name=category)
#             Task.objects.create(user=request.user, title=title, desciption = description, priority=priority, due_date=due_date, category=category)
        
#         return redirect('todo_list')
    
#     return render(request,'index.html')

@login_required(login_url='login')
def complete_todo(request, todo_id):
    todo = Task.objects.get(id=todo_id, user=request.user)
    todo.completed = True
    todo.save()
    return redirect('todo_list')

@login_required(login_url='login')
def delete_todo(request, todo_id):
    todo = Task.objects.get(id=todo_id, user=request.user)
    todo.delete()
    return redirect('todo_list')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not User.objects.filter(username=username, email=email).exists():
            messages.error(request,"Invalid username or password")
            return redirect('login')
        
        user = authenticate(username = username, email = email, password= password) # verifies and returns a User Object with credentials

        if user is None:    # Checks again for the returned User Object
            messages.error(request,"Invalid Credentials")
            return redirect('login')
        
        else:   # if the returned credential are valid it logs in the user
            login(request, user)
            return redirect('todo_list')
    
    
    return render(request,'login.html')
    
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username, email = email)
        
        if user.exists():
            messages.info(request, "User already taken")
            return redirect('register')
        
        user = User.objects.create_user(username=username, email = email)
        user.set_password(password)
        user.save()
        
        messages.info(request,"Account created successfully")
        
        return redirect('register')
    return render (request,'register.html')

def logout_page(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def edit_task(request, todo_id):
    
    task = Task.objects.get(id=todo_id)
    
    if request.method == 'POST':
        task.desciption = request.POST.get('description')
        task.title = request.POST.get('title')
        task.priority = request.POST.get('priority') or 1
        task.due_date = request.POST.get('due_date')
        # category = request.POST.get('category')
        category_name = request.POST.get('category')
        categories = Category.objects.filter(name=category_name)

        if categories.exists():
            category = categories.first()  # Get the first category found
        else:
        # Optionally create the category if it doesn't exist
            category = Category.objects.create(name=category_name)

        task.category = category
        task.save()
        return redirect('todo_list')
    
    return render(request, 'edit.html', {'task':task})

# @login_required(login_url='login')
# def get_title(request):
    
#     search = request.GET.get('search','')
#     payload = []

#     if search:
#         objs = Task.objects.filter(user=request.user,title__startswith=search)
#         for obj in objs:
#             print(f"obj {obj}")
#             payload.append({
#                 "title": obj.title
#             })
        
#     return JsonResponse({
#         "status": True,
#         "payload": payload
#     })
 