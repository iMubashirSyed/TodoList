from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task, Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

    
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
    
    if sort_by == 'due_date_desc':
        todos = todos.order_by('-due_date')
    elif sort_by == 'due_date_asc':
        todos = todos.order_by('due_date')
    elif sort_by == 'priority_asc':
        todos = todos.order_by('priority')
    elif sort_by == 'priority_desc':
        todos = todos.order_by('-priority')

    return render(request, 'index.html', {'todos': todos})
    
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
        Task.objects.create(user=request.user, title=title, desciption=description, priority=priority, due_date=due_date, category=category)
        
    return redirect('todo_list')

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
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid username or password")
            return redirect('login')
        
        user = authenticate(username = username, password= password) # verifies and returns a User Object with credentials

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
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, "User already taken")
            return redirect('register')
        
        user = User.objects.create_user(username=username)
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

@login_required(login_url='login')
def get_title(request):
    
    search = request.GET.get('search','')
    payload = []
    
    if search:
        objs = Task.objects.filter(user=request.user,title__startswith=search)
        for obj in objs:
            payload.append({
                "title": obj.title
            })
        
    return JsonResponse({
        "status": True,
        "payload": payload
    })

@login_required(login_url='login')
def get_title(request):
    search = request.GET.get('search', '')
    payload = []

    if search:
        # Filter tasks based on user and title containing the search string
        objs = Task.objects.filter(user=request.user, title__startswith=search)
        for obj in objs:
            payload.append({
                "title": obj.title
            })
        
    return JsonResponse({
        "status": True,
        "payload": payload
    })

        
    


 