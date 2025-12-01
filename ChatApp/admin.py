from django.contrib import admin
from .models import ChatApp, ChatConversation, ChatMessage, ChatRoom

# @admin.register(ChatApp)
# class ChatAppAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'city', 'phone', 'email', 'is_active', 'created_at']
#     list_filter = ['is_active', 'city', 'created_at']
#     search_fields = ['name', 'email', 'city']
#     readonly_fields = ['created_at']
#     ordering = ['name']

@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_chatapp_name', 'is_active', 'started_at', 'last_message_at']
    list_filter = ['is_active', 'started_at', 'last_message_at']
    search_fields = ['user__email', 'ChatApp__name']
    readonly_fields = ['started_at', 'last_message_at']
    ordering = ['-last_message_at']

    def get_chatapp_name(self, obj):
        return obj.ChatApp.name if obj.ChatApp else "Unknown"
    get_chatapp_name.short_description = 'ChatApp'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'conversation', 'sender', 'message_preview', 'is_read', 'sent_at']
    list_filter = ['is_read', 'sent_at']
    search_fields = ['sender__email', 'message_content']
    readonly_fields = ['sent_at']
    ordering = ['-sent_at']

    def message_preview(self, obj):
        return obj.message_content[:50] + '...' if len(obj.message_content) > 50 else obj.message_content
    message_preview.short_description = 'Message'

# @admin.register(ChatRoom)
# class ChatAppAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'created_at']
#     list_filter = ['created_at']
#     search_fields = ['name']
#     readonly_fields = ['created_at']
#     ordering = ['-created_at']
