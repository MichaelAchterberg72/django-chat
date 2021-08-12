from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
import json

from django.db.models import Count, Sum, F, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from csp.decorators import csp_exempt

from .models import ChatGroup, ChatRoomMembers, Message, MessageRead
from users.models import CustomUser


@login_required()
@csp_exempt
def index(request):
    username = request.user
    user_name = username.user_name
    groups_qs = ChatRoomMembers.objects.filter(talent=username).order_by('-date_modified').values_list('chat_group')

    chat_rooms = {}
    for item in groups_qs:
        groups = ChatRoomMembers.objects.filter(Q(talent=username) & Q(chat_group=item)).values_list('room_name', 'date_modified', 'chat_group__slug')
        messages_received = MessageRead.objects.filter(Q(chat_group=item) & Q(message_read=False) & Q(talent=username)).count()

        chat_rooms[item] = {'group': groups, 'notification': messages_received}
#        chat_rooms.append(result)


    template_name = 'chat/menu.html'
    context = {
            'user_name': user_name,
            'chat_rooms': chat_rooms,
    }
    return render(request, template_name, context)


@login_required()
@csp_exempt
def room(request, room_name):

    room = ChatRoomMembers.objects.filter(Q(chat_group__slug=room_name) & Q(talent=request.user)).values_list('room_name', flat=True)

    template_name = 'chat/room.html'
    context = {
            'room': room,
            'room_name_json': mark_safe(json.dumps(room_name)),
            'username': mark_safe(json.dumps(request.user.username))
    }
    return render(request, template_name, context)


def new_chat_view(request, tlt):
    own_chat = ChatRoomMembers.objects.filter(Q(talent=request.user) & Q(room_name=tlt))
    other_chat = ChatRoomMembers.objects.filter(Q(talent__username=tlt) & Q(room_name=request.user.username))
    custom_user = CustomUser.objects.get(username=tlt)

    if request.method == 'POST':
        if other_chat:
            if own_chat:
                chat_room = own_chat.values_list('chat_group__slug', flat=True)[0]
                own_chat.update(date_modified=timezone.now())
                other_chat.update(date_modified=timezone.now())

                return redirect(reverse('Chat:room', kwargs={'room_name': chat_room}))

            else:
                create_new_chat_group = ChatGroup.objects.create(room_name='New Chat')
                chat_group = ChatGroup.objects.latest('date_created')
                create_own_chat = ChatRoomMembers.objects.create(
                        talent=request.user,
                        chat_group=chat_group,
                        room_name=tlt,
                        date_modified=timezone.now())
                create_other_chat = ChatRoomMembers.objects.create(
                        talent=custom_user,
                        chat_group=chat_group,
                        room_name=request.user.username,
                        date_modified=timezone.now())

                return redirect(reverse('Chat:room', kwargs={'room_name': chat_group.slug}))

        else:
            create_new_chat_group = ChatGroup.objects.create(room_name='New Chat')
            chat_group = ChatGroup.objects.latest('date_created')
            create_own_chat = ChatRoomMembers.objects.create(
                    talent=request.user,
                    chat_group=chat_group,
                    room_name=tlt,
                    date_modified=timezone.now())
            create_other_chat = ChatRoomMembers.objects.create(
                    talent=custom_user,
                    chat_group=chat_group,
                    room_name=request.user.username,
                    date_modified=timezone.now())

            return redirect(reverse('Chat:room', kwargs={'room_name': chat_group.slug}))
