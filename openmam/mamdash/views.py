from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Video, User
import bcrypt
import os


from .forms import UploadFileForm


def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'videos': Video.objects.all()
        }
        return render(request, 'dashboard.html', context)

def registration(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        
        return redirect('/register')
    else:
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        Login = User(first_name=firstname, last_name=lastname, email=email, password=pw_hash)
        Login.save()
        messages.success(request, "Login Created")

        return redirect("/login")

def trylogin(request):
    user = User.objects.filter(email=request.POST['email'])
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['admin'] = logged_user.admin
            return redirect('/dashboard')
    return redirect("/login")

def show_users(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'users': User.objects.all()
        }
        return render(request, 'usermanager.html', context)

def deleteuser(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()

    return redirect('/showusers')

def deletevideo(request, video_id):
    video = Video.objects.get(id=video_id)
    video.delete()
    # os.remove(video.filepath.path)

    return redirect('/dashboard')

def favoritevideo(request, video_id):
    video = Video.objects.get(id=video_id)
    user = User.objects.get(id=request.session["user_id"])
    user.favorited_by.add(video)

    return redirect('/dashboard')

def unfavoritevideo(request, video_id):
    video = Video.objects.get(id=video_id)
    user = User.objects.get(id=request.session["user_id"])
    user.favorited_by.remove(video)

    return redirect('/dashboard')

def edit_video(request, video_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            'video': Video.objects.get(id=video_id),
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, "edit_video.html", context)

def update_video(request, video_id):
    video = Video.objects.get(id=video_id)
    video.details = request.POST['details']
    video.title = request.POST['title']
    video.save()

    return redirect('/dashboard')

def adminonly(request, video_id):
    video = Video.objects.get(id=video_id)
    video.restricted = request.POST['adminaccess']
    video.save()

    return redirect('/dashboard')

def logout(request):
    request.session.flush()

    return redirect('/')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(id=request.session["user_id"])
            instance = Video(filepath=request.FILES['file'],uploaded_by=user,title=request.POST['title'])
            instance.save()
            return redirect('/dashboard')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

