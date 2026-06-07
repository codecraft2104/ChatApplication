from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

from .models import (
    Message, Profile, Contact,
    Status, Report,
    Group, GroupMessage
)

from django.utils.timezone import now, timedelta
from django.db.models import Count


# ================= AUTH =================

def user_login(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']

        try:
            profile = Profile.objects.get(hg_id=user_id)
            user = authenticate(request,
                username=profile.user.username,
                password=password
            )

            if user:
                login(request, user)
                profile.is_online = True
                profile.save()
                return redirect('dashboard')

        except Profile.DoesNotExist:
            pass

        return render(request, 'chat/login.html', {'error': 'Invalid credentials'})

    return render(request, 'chat/login.html')


def user_logout(request):
    try:
        request.user.profile.is_online = False
        request.user.profile.save()
    except:
        pass

    logout(request)
    return redirect('login')
def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        bio = request.POST['bio']

        # ❌ check duplicate username
        if User.objects.filter(username=username).exists():
            return render(request, 'chat/register.html', {
                'error': 'Username already exists'
            })

        # ✅ create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        # ✅ create profile (IMPORTANT)
        profile = Profile.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            phone=phone,
            bio=bio
        )

        # ✅ NOW profile exists → safe to use
        return render(request, 'chat/register_success.html', {
            'user_id': profile.hg_id
        })

    return render(request, 'chat/register.html')

# ================= DASHBOARD =================

def dashboard(request):
    contacts = Contact.objects.filter(user=request.user)

    chat_list = []

    # PRIVATE CHATS
    for c in contacts:
        last_msg = Message.objects.filter(
            sender__in=[request.user, c.contact_user],
            receiver__in=[request.user, c.contact_user]
        ).order_by('-timestamp').first()

        unread = Message.objects.filter(
            sender=c.contact_user,
            receiver=request.user,
            is_read=False
        ).count()

        chat_list.append({
            'type': 'private',
            'user': c.contact_user,
            'last_msg': last_msg,
            'unread': unread
        })

    # GROUP CHATS
    groups = request.user.chat_groups.all()

    for g in groups:
        last_msg = GroupMessage.objects.filter(group=g).order_by('-timestamp').first()

        chat_list.append({
            'type': 'group',
            'group': g,
            'last_msg': last_msg,
            'unread': 0
        })

    chat_list.sort(
        key=lambda x: x['last_msg'].timestamp if x['last_msg'] else now(),
        reverse=True
    )

    return render(request, 'chat/dashboard.html', {
        'users': chat_list
    })


# ================= PRIVATE CHAT =================

import os
from .models import Message, Contact

def chat_view(request, user_id):
    receiver = User.objects.get(id=user_id)

    # ✅ MARK READ
    Message.objects.filter(
        sender=receiver,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    # ✅ CHAT MESSAGES
    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    # ✅ CONTACT LIST (IMPORTANT FIX)
    contacts = Contact.objects.filter(user=request.user)

    users = []
    
    # PRIVATE CHATS
    for c in contacts:
        if c.contact_user:

            last_msg = Message.objects.filter(
                sender__in=[request.user, c.contact_user],
                receiver__in=[request.user, c.contact_user]
            ).order_by('-timestamp').first()

            unread = Message.objects.filter(
                sender=c.contact_user,
                receiver=request.user,
                is_read=False
            ).count()

            users.append({
                'type': 'private',
                'user': c.contact_user,
                'last_msg': last_msg,
                'unread': unread
            })
    
    # GROUP CHATS
    groups = request.user.chat_groups.all()
    
    for g in groups:
        last_msg = GroupMessage.objects.filter(group=g).order_by('-timestamp').first()
        
        users.append({
            'type': 'group',
            'group': g,
            'last_msg': last_msg,
            'unread': 0
        })
    
    users.sort(
        key=lambda x: x['last_msg'].timestamp if x['last_msg'] else now(),
        reverse=True
    )

    return render(request, 'chat/dashboard.html', {
        'users': users,
        'messages': messages,
        'receiver': receiver
    })

def send_message(request):
    if request.method == "POST":
        receiver_id = request.POST.get("receiver")
        message = request.POST.get("message")
        file = request.FILES.get("file")

        receiver = User.objects.get(id=receiver_id)

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message or "",
            file=file
        )

        # ✅ AUTO-SAVE CONTACTS (PERSISTENT)
        # Save sender's contact (sender has receiver in contacts)
        Contact.objects.get_or_create(
            user=request.user,
            contact_user=receiver
        )

        # Save receiver's contact (receiver has sender in contacts)
        Contact.objects.get_or_create(
            user=receiver,
            contact_user=request.user
        )

    return redirect('chat', user_id=receiver_id)


# ================= SEARCH & CONTACT =================

def search_user(request):
    if request.method == 'POST':
        hg_id = request.POST.get('hg_id')

        try:
            profile = Profile.objects.get(hg_id=hg_id)

            # ✅ auto save contact
            Contact.objects.get_or_create(
                user=request.user,
                contact_user=profile.user
            )

            return redirect('chat', user_id=profile.user.id)

        except Profile.DoesNotExist:
            return redirect('dashboard')

def save_contact(request, user_id):
    user = User.objects.get(id=user_id)

    Contact.objects.get_or_create(
        user=request.user,
        contact_user=user
    )

    return redirect('chat', user_id=user_id)


# ================= PROFILE =================

def profile_view(request):
    return render(request, 'chat/profile.html', {
        'profile': request.user.profile
    })


def edit_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.full_name = request.POST['full_name']
        profile.email = request.POST['email']
        profile.phone = request.POST['phone']
        profile.bio = request.POST['bio']

        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES['profile_pic']

        profile.save()
        return redirect('profile')

    return render(request, 'chat/edit_profile.html', {'profile': profile})


# ================= STATUS =================

def add_status(request):
    if request.method == "POST":
        Status.objects.create(
            user=request.user,
            text=request.POST.get("text"),
            image=request.FILES.get("image")
        )
        return redirect('my_statuses')
    return redirect('dashboard')


def view_my_statuses(request):
    """View all my statuses"""
    my_statuses = Status.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'chat/my_statuses.html', {
        'statuses': my_statuses
    })


def view_status(request, status_id):
    """View a single status with full details"""
    status = get_object_or_404(Status, id=status_id)
    
    # Add current user as viewer
    if request.user != status.user:
        status.viewers.add(request.user)
    
    return render(request, 'chat/view_status.html', {
        'status': status
    })


def view_contacts_status(request):
    """View all contacts and their latest status"""
    contacts = Contact.objects.filter(user=request.user).select_related('contact_user')
    
    contacts_with_status = []
    for contact in contacts:
        latest_status = Status.objects.filter(
            user=contact.contact_user
        ).order_by('-created_at').first()
        
        contacts_with_status.append({
            'contact': contact.contact_user,
            'status': latest_status,
            'saved_name': contact.saved_name or contact.contact_user.username
        })
    
    return render(request, 'chat/contacts_status.html', {
        'contacts_with_status': contacts_with_status
    })


def view_contact_profile(request, user_id):
    """View a contact's profile with status"""
    contact_user = get_object_or_404(User, id=user_id)
    contact_profile = contact_user.profile
    
    # Get latest status
    latest_status = Status.objects.filter(
        user=contact_user
    ).order_by('-created_at').first()
    
    # Get all non-expired statuses
    all_statuses = Status.objects.filter(
        user=contact_user,
        
    ).order_by('-created_at')
    
    return render(request, 'chat/contact_profile.html', {
        'contact_profile': contact_profile,
        'latest_status': latest_status,
        'all_statuses': all_statuses
    })


# ================= REPORT =================

def report_message(request, msg_id):
    msg = get_object_or_404(Message, id=msg_id)

    if msg.sender == request.user:
        return redirect('dashboard')

    if Report.objects.filter(message=msg, reported_by=request.user).exists():
        return redirect('dashboard')

    Report.objects.create(message=msg, reported_by=request.user)

    return redirect('dashboard')


# ================= GROUPS =================

def groups_view(request):
    groups = request.user.chat_groups.all()
    return render(request, 'chat/groups.html', {'groups': groups})


def create_group(request):
    if request.method == "POST":
        name = request.POST['name']
        group = Group.objects.create(name=name, admin=request.user)
        group.members.add(request.user)
        return redirect('groups')

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/create_group.html', {'users': users})


def group_chat(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == "POST":
        GroupMessage.objects.create(
            group=group,
            sender=request.user,
            message=request.POST.get("message"),
            file=request.FILES.get("file")
        )

    messages = GroupMessage.objects.filter(group=group).order_by('timestamp')

    # ✅ BUILD CHAT LIST FOR SIDEBAR
    contacts = Contact.objects.filter(user=request.user)

    chat_list = []
    
    # PRIVATE CHATS
    for c in contacts:
        if c.contact_user:
            last_msg = Message.objects.filter(
                sender__in=[request.user, c.contact_user],
                receiver__in=[request.user, c.contact_user]
            ).order_by('-timestamp').first()

            unread = Message.objects.filter(
                sender=c.contact_user,
                receiver=request.user,
                is_read=False
            ).count()

            chat_list.append({
                'type': 'private',
                'user': c.contact_user,
                'last_msg': last_msg,
                'unread': unread
            })
    
    # GROUP CHATS
    groups = request.user.chat_groups.all()
    
    for g in groups:
        last_msg = GroupMessage.objects.filter(group=g).order_by('-timestamp').first()
        
        chat_list.append({
            'type': 'group',
            'group': g,
            'last_msg': last_msg,
            'unread': 0
        })
    
    chat_list.sort(
        key=lambda x: x['last_msg'].timestamp if x['last_msg'] else now(),
        reverse=True
    )

    # ✅ GET GROUP MEMBERS
    group_members = group.members.all()

    return render(request, 'chat/group_chat.html', {
        'group': group,
        'messages': messages,
        'chat_list': chat_list,
        'group_members': group_members
    })


def add_member(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.user != group.admin:
        return redirect('group_chat', group_id=group_id)

    if request.method == "POST":
        user = User.objects.get(id=request.POST.get('user'))
        group.members.add(user)

    users = User.objects.exclude(id__in=group.members.all())

    return render(request, 'chat/add_member.html', {
        'group': group,
        'users': users
    })


# ================= ADMIN =================

def admin_only(user):
    return user.is_staff



import json
from django.http import JsonResponse

@user_passes_test(admin_only)
def admin_dashboard(request):
    stats = {
        "total_users": User.objects.count(),
        "total_messages": Message.objects.count(),
        "total_reports": Report.objects.count(),
        "total_status": Status.objects.count(),
    }

    return render(request, "chat/admin/dashboard.html", {
        "stats_json": json.dumps([
            stats["total_users"],
            stats["total_messages"],
            stats["total_reports"],
            stats["total_status"],
        ]),
        "total_users": stats["total_users"],
        "total_messages": stats["total_messages"],
        "total_reports": stats["total_reports"],
        "total_status": stats["total_status"],
    })


@user_passes_test(admin_only)
def admin_users(request):
    return render(request, 'chat/admin/admin_users.html', {
        'users': User.objects.all()
    })


@user_passes_test(admin_only)
def admin_chats(request):
    return render(request, 'chat/admin/admin_chats.html', {
        'messages': Message.objects.all().order_by('-timestamp')
    })


@user_passes_test(admin_only)
def admin_reports(request):
    return render(request, 'chat/admin/admin_reports.html', {
        'reports': Report.objects.all()
    })


@user_passes_test(admin_only)
def admin_status(request):
    return render(request, 'chat/admin/admin_status.html', {
        'statuses': Status.objects.all()
    })


@user_passes_test(admin_only)
def admin_groups(request):
    return render(request, 'chat/admin/admin_groups.html', {
        'groups': Group.objects.all()
    })


def delete_message(request, id):
    Message.objects.get(id=id).delete()
    return redirect('admin_chats')


def delete_status(request, id):
    Status.objects.get(id=id).delete()
    return redirect('admin_status')


def delete_group(request, id):
    Group.objects.get(id=id).delete()
    return redirect('admin_groups')


def ban_user(request, id):
    u = User.objects.get(id=id)
    u.is_active = False
    u.save()
    return redirect('admin_users')


def unban_user(request, id):
    u = User.objects.get(id=id)
    u.is_active = True
    u.save()
    return redirect('admin_users')


@user_passes_test(admin_only)
def admin_send_message(request, user_id):
    """Admin sends a message to a user (for warnings/instructions after report)"""
    if request.method == "POST":
        receiver = User.objects.get(id=user_id)
        message_text = request.POST.get("message")

        # Create message from admin system account or admin user
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            message=f"[⚠️ ADMIN]: {message_text}"
        )

    return redirect('admin_reports')


from django.contrib.auth import authenticate, login
from django.contrib import messages

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Admin access only!")

    return render(request, 'chat/admin_login.html')

from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Message, Report, Status

def live_stats(request):
    data = {
        "total_users": User.objects.count(),
        "total_messages": Message.objects.count(),
        "total_reports": Report.objects.count(),
        "total_status": Status.objects.count(),
    }
    return JsonResponse(data)

from django.db.models import Count
from django.utils.timezone import now, timedelta

def analytics(request):
    today = now().date()

    data = {
        "today_users": User.objects.filter(date_joined__date=today).count(),
        "today_messages": Message.objects.filter(timestamp__date=today).count(),
    }
    return JsonResponse(data)

def send_admin_alert(message):
    # later upgrade to websocket push
    print("ALERT:", message)