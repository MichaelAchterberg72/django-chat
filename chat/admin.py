from django.contrib import admin

from .models import Message, ChatGroup, ChatRoomMembers, MessageRead


@admin.register(MessageRead)
class MessageReadAdmin(admin.ModelAdmin):
    model = MessageRead

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model = Message

@admin.register(ChatGroup)
class ChatGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(ChatRoomMembers)
class ChatRoomMembersAdmin(admin.ModelAdmin):
    pass
