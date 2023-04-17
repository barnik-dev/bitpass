from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q 

from .models import User, Categories, SavedPassword

from .misc import greet_user, encryption


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'base/home.html')


def userSignup(request):
    signup_error = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = None
        try:
            user = User.objects.create_user(email=email, password=password, name=name)
        except:
            signup_error = True

        if user is not None:
            user.save()
            login(request, user)
            return redirect('dashboard')

    return render(request, 'base/signup.html', {'signup_error': signup_error})


def userLogin(request):
    login_error = False

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            login_error = True 
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            login_error = True

    return render(request, 'base/login.html', {'login_error':login_error})


@login_required(login_url='home')
def userLogout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    current_user = request.user
    categories = current_user.categories_set.all()
    greet = greet_user.greet()
    q = request.GET.get('q') if request.GET.get('q') != None else '' #FOR SEARCH BASED ON SEARCH FORM
    r = request.GET.get('r') if request.GET.get('r') != None else '' #FOR SEARCH BASED ON CATEGORIES

    if q != "":
        passwords = current_user.savedpassword_set.filter(
            Q(category__category_name__icontains=q) |
            Q(title__icontains=q) |
            Q(email__icontains=q) |
            Q(description__icontains=q) 
        ) 
    elif r != "":
        passwords = current_user.savedpassword_set.filter(
            category__category_name__icontains=r
        )
    else:
        passwords = current_user.savedpassword_set.all() 
    saved_passwords = []

    for i in range(len(passwords)):
        password_model = {}
        password_model['id'] = passwords[i].id
        password_model['title'] = passwords[i].title
        password_model['email'] = passwords[i].email
        password_model['description'] = passwords[i].description[:35]
        password_model['saved_password'] = encryption.decrypt(passwords[i].saved_password)

        saved_passwords.append(password_model)

    
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        print(category_name)
        category, created = Categories.objects.get_or_create(category_name=category_name, user=current_user)
        return redirect('dashboard')

    context = {'greet': greet, 'categories': categories, 'saved_passwords': saved_passwords}

    return render(request, 'base/dashboard.html', context)

@login_required(login_url='login')
def addPassword(request):
    current_user = request.user
    categories = current_user.categories_set.all()
    greet = greet_user.greet()

    if request.method == 'POST':
        title = request.POST.get('title')
        email = request.POST.get('email')
        password = encryption.encrypt(request.POST.get('saved_password'))
        category_name = request.POST.get('category')
        description = request.POST.get('description')

        category, created = Categories.objects.get_or_create(category_name=category_name, user=current_user)
        save_password = SavedPassword.objects.create(
            user = current_user,
            title=title,
            email=email,
            description=description,
            saved_password=password,
            category=category
        )
        save_password.save()
        return redirect('dashboard')
    return render(request, 'base/add-password.html', {'greet': greet, 'categories': categories})

@login_required(login_url='login')
def editPassword(request, pk):
    password = SavedPassword.objects.get(id=pk)

    if request.user != password.user:
        return redirect('dashboard')

    decrypted_password = encryption.decrypt(password.saved_password)
    greet = greet_user.greet()

    if request.method == 'POST':
        password.title = request.POST.get('title')
        password.email = request.POST.get('email')
        password.saved_password = encryption.encrypt(request.POST.get('saved_password'))
        password.description = request.POST.get('description')

        category_name = request.POST.get('category')
        category, created = Categories.objects.get_or_create(category_name=category_name, user=request.user)
        password.category = category

        password.save()
        return redirect('dashboard')

    context = {'password': password, 'decrypted_password': decrypted_password, 'greet': greet}
    return render(request, 'base/add-password.html', context)

@login_required(login_url='login')
def deletePassword(request, pk):
    password = SavedPassword.objects.get(id=pk)

    if request.user != password.user:
        return redirect('dashboard')

    if request.method == 'POST':
        password.delete()
        return redirect('dashboard')
    
    return render(request, 'base/delete.html', {'password': password})

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    greet = greet_user.greet()
    edit_error = False

    if request.method == 'POST':
        try:
            user.name = request.POST.get('name')
            user.email = request.POST.get('email')
            user.save()
        except:
            edit_error = True

        if not edit_error:
            return redirect('dashboard')

    context = {'greet': greet, 'user': user, 'edit_error': edit_error}
    return render(request, 'base/edit-profile.html', context)

@login_required(login_url='login')
def deleteUser(request):
    user = request.user
    delete = "User"

    if request.method == 'POST':
        user.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'delete': delete})