from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Albums,Songs
from django.db.models import Count

# Create your views here.
@login_required(login_url="login")
def detail(request):
    album = Albums.objects.count()
    song = Songs.objects.filter(album_id__in=Albums.objects.all()).count()
    print(song)
    content = {
        'album':album,
        'song':song
    }
    return render(request,"details.html",context=content)

@login_required(login_url="login")
def search(request):
    query = request.GET["query"]
    result=[]
    if query:
        result=Albums.objects.annotate(no_songs=Count("song_name")).filter(album__icontains=query)
        return render(request,"search.html",{"results":result})
    else:
        return render(request,"search.html")

@login_required(login_url="login")
def song_list(request,al):
    album = Albums.objects.filter(album=al).first()
    songs = Songs.objects.filter(album_id=al)
    content = {
        "album":album,
        "songs":songs,
    }
    return render(request,"song_list.html",content)


@login_required(login_url="login")
def music(request,song_name):
    songs = Songs.objects.filter(song_name=song_name).first()
    album = songs.album_id
    duration = songs.durations.replace("min","").strip()
    songs.durations = duration
    album = Albums.objects.filter(album=album).first()
    content = {
        "album":album,
        "songs":songs,
    }
    return render(request,"music.html",content)


@login_required(login_url="login")
def index(request):
    album = Albums.objects.annotate(no_song=Count("song_name")).all()
    content = {'album':album}
    return render(request,"index.html",content)

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Invalid credentials")
            return redirect("login")

    else:    
        return render(request,"login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email exists")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username exists")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()

                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                return redirect("/")
            
        else:
            messages.info(request, "Password not match")
            return redirect('signup')

    else:
        return render(request,"signup.html")

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("login")
