from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from .models import Message, Notification, UserPresence


@login_required
def dashboard(request):
    users = User.objects.exclude(id=request.user.id).order_by('username')
    presence_map = {presence.user_id: presence for presence in UserPresence.objects.select_related('user')}

    user_cards = []
    for user in users:
        unread_count = Message.objects.filter(sender=user, receiver=request.user, is_read=False).count()
        latest_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) | Q(sender=user, receiver=request.user)
        ).order_by('-created_at').first()
        user_cards.append({
            'user': user,
            'presence': presence_map.get(user.id),
            'unread_count': unread_count,
            'latest_message': latest_message,
        })

    notifications = Notification.objects.filter(user=request.user, is_seen=False).select_related('message')[:10]
    total_unread_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

    return render(request, 'chat/dashboard.html', {
        'user_cards': user_cards,
        'notifications': notifications,
        'total_unread_notifications': total_unread_notifications,
    })


@login_required
def room(request, username):
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver').order_by('created_at')

    unread_messages = messages.filter(sender=other_user, receiver=request.user, is_read=False)
    unread_messages.update(is_read=True)
    Notification.objects.filter(user=request.user, message__in=unread_messages).update(is_seen=True)

    current_presence = UserPresence.objects.filter(user=other_user).first()
    sidebar_users = User.objects.exclude(id=request.user.id).order_by('username')

    return render(request, 'chat/room.html', {
        'other_user': other_user,
        'messages': messages,
        'presence': current_presence,
        'sidebar_users': sidebar_users,
    })
