# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('send/', views.send_message, name='send_message'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path("admin/live-stats/", views.live_stats, name="live_stats"),
    # chat/urls.py
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('search/', views.search_user, name='search_user'),
    path('save-contact/<int:user_id>/', views.save_contact, name='save_contact'),
    path('add-status/', views.add_status, name='add_status'),
    path('my-statuses/', views.view_my_statuses, name='my_statuses'),
    path('status/<int:status_id>/', views.view_status, name='view_status'),
    path('contacts-status/', views.view_contacts_status, name='contacts_status'),
    path('contact/<int:user_id>/', views.view_contact_profile, name='contact_profile'),
    path('report/<int:msg_id>/', views.report_message, name='report_message'),   
    path('admin-login/', views.admin_login, name='admin_login'),
    path('panel/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('panel/users/', views.admin_users, name='admin_users'),
    path('panel/chats/', views.admin_chats, name='admin_chats'),
    path('panel/reports/', views.admin_reports, name='admin_reports'),
    path('panel/status/', views.admin_status, name='admin_status'),
    path('panel/delete-message/<int:id>/', views.delete_message, name='delete_message'),
    path('panel/delete-status/<int:id>/', views.delete_status, name='delete_status'),

    path('panel/groups/', views.admin_groups, name='admin_groups'),
    path('panel/delete-group/<int:id>/', views.delete_group, name='delete_group'),
    path('panel/ban/<int:id>/', views.ban_user, name='ban_user'),
    path('panel/unban/<int:id>/', views.unban_user, name='unban_user'),
    path('panel/send-message/<int:user_id>/', views.admin_send_message, name='admin_send_message'),
    path('groups/', views.groups_view, name='groups'),
    path('group/create/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_chat, name='group_chat'),
    path('group/add-member/<int:group_id>/', views.add_member, name='add_member'),
]