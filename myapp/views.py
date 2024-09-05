import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from .forms import LoginForm, SignUpForm, EventForm, ProfileForm
from .models import MyUser, Event, Comment, Notification
from django.utils import timezone
from django.core.mail import send_mail
from django.http import JsonResponse
import random
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,  PageNotAnInteger, EmptyPage
from .models import Notification


def login_view(request):
    if request.method == "POST":
        usernm = request.POST.get("username")
        passwd = request.POST.get("password")

        user = authenticate(request, username=usernm, password=passwd)

        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            messages.error(request, "Invalid username or email, or incorrect password. Please try again.")
            return redirect('login') 
    else:
        form = LoginForm()

    return render(request, "myapp/login.html", {"form": form})
        

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            stored_code = request.session.get('verification_code')
            code_sent_at = request.session.get('code_sent_at')
            print(stored_code, code_sent_at, form.cleaned_data['verification_code'])

            if stored_code and code_sent_at:
                elapsed_time = timezone.now().timestamp() - code_sent_at
                if elapsed_time > 6000:
                    form.add_error('verification_code', 'Verification code has expired.')
                elif str(stored_code) != str(form.cleaned_data['verification_code']):
                    form.add_error('verification_code', 'Invalid verification code.')
                else:
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    user = MyUser.objects.create_user(username=username, email=email, password=password)
                    user.save()

                    messages.success(request, 'Sign up successful!')
                    return redirect('login') 
        else:
            messages.error(request, 'Please correct the errors below.')
        print(form.errors)
        return render(request, 'myapp/signup.html', {'form': form}) 

    else:
        form = SignUpForm()

    return render(request, 'myapp/signup.html', {'form': form})

def send_verification_code(request):
    if request.method == 'POST':
        print(request.body)
        # email = request.POST.get('email')
        data = json.loads(request.body)
        email = data.get("email")
        if email:
            code = random.randint(100000, 999999) 

            send_mail(
                'Your verification code',
                f'Your verification code is {code}',
                'zhang0129pia@gmail.com',
                [email],
                fail_silently=False,
            )

            request.session['verification_code'] = code
            request.session['code_sent_at'] = timezone.now().timestamp()

            return JsonResponse({'status': 'ok', 'message': 'Verification code sent'})
        return JsonResponse({'status': 'error', 'message': 'Invalid email'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def custom_logout_view(request):
    logout(request)
    return redirect('homepage')

def profile_view(request, username=None):
    if username:
        user = get_object_or_404(MyUser, username=username)
    else:
        user = request.user

    is_editing = request.GET.get('edit') == 'true' and user == request.user
    next_url = request.GET.get('next')
    if request.method == 'POST' and user == request.user:
        form = ProfileForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            if request.POST.get('remove_avatar') == "true":
                if user.profile_picture and user.profile_picture.name != 'profile_pictures/default_avatar.png':
                    user.profile_picture.delete(save=False)
                user.profile_picture = 'profile_pictures/default_avatar.png'
            else:
                if 'profile_picture' in request.FILES:
                    user.profile_picture = request.FILES['profile_picture']
            
            form.save()
            return redirect('profile', username=user.username)
        else:
            return render(request, 'myapp/profile.html', {
                'form': form,
                'user': user,
                'is_editing': is_editing,
                'next_url': next_url,
                'errors': form.errors
            })
    else:
        form = ProfileForm(instance=user)
    
    return render(request, 'myapp/profile.html', {
        'form': form,
        'user': user,
        'is_editing': is_editing,
        'next_url': next_url
    })


@login_required(login_url='login') 
def create_event(request):
    if request.method =='POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_detail', pk=event.id)
        
    else:
        form = EventForm()
    return render(request, 'myapp/create_event.html', {'form': form})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = Comment.objects.filter(event=event, parent__isnull=True).order_by('-created_at').prefetch_related('replies')
    context = {
        'event': event,
        'comments': comments,
        'is_favorite': event.saved_by_users.filter(id=request.user.id).exists() if request.user.is_authenticated else False,
    }
    return render(request, 'myapp/event_detail.html', context)


@login_required(login_url='login')
def toggle_favorite(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user in event.saved_by_users.all():
        event.saved_by_users.remove(request.user) #remove it from saved events
        is_favorite = False
    else:
        event.saved_by_users.add(request.user)
        is_favorite = True
    return JsonResponse({'is_favorite': is_favorite})


@login_required(login_url='login')
def apply_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user in event.applied_by_users.all():
        event.applied_by_users.remove(request.user)
        event.update_current_participants()
        applied = False
    else:
        event.applied_by_users.add(request.user)
        event.update_current_participants()
        applied = True
    return JsonResponse({
        'applied': applied,
        'current_participants':
        event.current_participants,
        })


def paginate_events(request, events_list, per_page=8):
    paginator = Paginator(events_list, per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # if page not integer，show page 1
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # if page out of range, show the last page
    
    return page_obj


def homepage(request):
    events = Event.objects.all().order_by('-created_at')
    page_obj = paginate_events(request, events)
    return render(request, 'myapp/homepage.html', {
        'page_obj': page_obj,
    })


def search_results(request):
    search_query = request.GET.get('search_query', '')
    location_query = request.GET.get('location', '')

    # Check if the search query matches the category or the title
    events = Event.objects.filter(
        Q(title__icontains=search_query) |
        Q(category__icontains=search_query)  # Assuming category is stored as a text field
    )

    # Apply location filter if provided
    if location_query:
        events = events.filter(location__icontains=location_query)

    events = events.order_by('-created_at')
    page_obj = paginate_events(request, events)

    return render(request, 'myapp/search_results.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'location_query': location_query,
    })


def filtered_events(request, category):
    events = Event.objects.filter(category__iexact=category).order_by('-created_at')
    page_obj = paginate_events(request, events)
    return render(request, 'myapp/filtered_events.html', {
        'page_obj': page_obj,
        'category': category,
    })


@login_required(login_url='login')
def saved_events(request):
    saved_events = request.user.saved_events.all().order_by('-created_at')
    page_obj = paginate_events(request, saved_events.all())
    return render(request, 'myapp/saved_events.html', {'page_obj': page_obj})


@login_required(login_url='login')
def upcoming_events(request):
    page_obj = paginate_events(request, request.user.upcoming_events.all().order_by('-created_at'))
    return render(request, 'myapp/upcoming_events.html', {'page_obj': page_obj})


@login_required(login_url='login')
def my_events(request):
    page_obj = paginate_events(request, Event.objects.filter(created_by=request.user).order_by('-created_at'))
    return render(request, 'myapp/my_events.html', {'page_obj': page_obj})


@login_required(login_url='login')
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form, 'event': event})


@login_required(login_url='login')
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == "POST":
        event.delete()
        return JsonResponse({'status': 'success', "message": "Event deleted successfully."}, status=200)
    return JsonResponse({'status': 'error', "message": "Invalid request."}, status=400)

@login_required(login_url='login')
def cancel_collection(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        request.user.saved_events.remove(event)
        return JsonResponse({'status': 'success', 'message': 'Event removed from saved events'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required(login_url='login')
def cancel_application(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        if request.user in event.applied_by_users.all():
            event.applied_by_users.remove(request.user)
            event.update_current_participants()
        request.user.upcoming_events.remove(event)
        return JsonResponse({'status': 'success', 'current_participants': event.current_participants})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


#Comment and notification
def post_comment(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            is_creator_reply = request.user == event.created_by
            Comment.objects.create(
                event=event, 
                user=request.user, 
                content=content, 
                is_creator_reply=is_creator_reply
            )
    return redirect('event_detail', event_id=event_id)

def add_comment(request, event_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        
        if not content:
            return JsonResponse({'status': 'error', 'message': 'Content cannot be empty'}, status=400)

        event = get_object_or_404(Event, id=event_id)
        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

        if parent_comment and parent_comment.user == request.user:
            return JsonResponse({'status': 'error', 'message': 'Cannot reply to your own comment'}, status=400)

        comment = Comment.objects.create(
            event=event,
            user=request.user,
            content=content,
            parent=parent_comment
        )

        return JsonResponse({
            'status': 'success',
            'comment': comment.content,
            'user': comment.user.username,
            'created_at': comment.created_at.strftime('%B %d, %Y, %I:%M %p'),
            'is_reply': bool(parent_comment)
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@require_POST
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id, recipient=request.user)
    notification.read = True
    notification.save()
    return JsonResponse({'success': 'Notification marked as read'})

def get_notifications(request):
    notifications = request.user.notifications.filter(read=False)
    data = [{
        'id': n.id,
        'message': n.message,
        'url': n.event.get_absolute_url(),
    } for n in notifications]

    unread_count = request.user.notifications.filter(read=False).count()

    response_data = {
        'notifications': data,
        'unread_count': unread_count
    }

    return JsonResponse(response_data)

