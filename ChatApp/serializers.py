from rest_framework import serializers
from .models import ChatConversation, ChatMessage, ChatApp
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatAppSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = ChatApp
        fields = ['id', 'name', 'address', 'city', 'phone', 'email', 'is_active']
        read_only_fields = ['id']


class ChatMessageSerializer(serializers.ModelSerializer):
    """Chat message serializer"""
    
    sender_name = serializers.SerializerMethodField()
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'conversation', 'sender', 'sender_name',
            'message_content', 'sender_type', 'sent_at', 
            'is_read', 'time_ago'
        ]
        read_only_fields = ['id', 'conversation', 'sender', 'sent_at']
    
    def get_sender_name(self, obj):
        """Get sender's full name"""
        if hasattr(obj.sender, 'first_name') and hasattr(obj.sender, 'last_name'):
            return f"{obj.sender.first_name} {obj.sender.last_name}"
        return obj.sender.email
    
    def get_time_ago(self, obj):
        """Human readable time"""
        from datetime import timedelta
        diff = timezone.now() - obj.sent_at
        
        if diff < timedelta(minutes=1):
            return "Just now"
        elif diff < timedelta(hours=1):
            minutes = int(diff.total_seconds() / 60)
            return f"{minutes}m ago"
        elif diff < timedelta(days=1):
            hours = int(diff.total_seconds() / 3600)
            return f"{hours}h ago"
        else:
            return obj.sent_at.strftime('%b %d')


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    """Create message serializer"""
    
    class Meta:
        model = ChatMessage
        fields = ['message_content', 'sender_type']
    
    def validate_message_content(self, value):
        """Validate message"""
        if not value or not value.strip():
            raise serializers.ValidationError("Message cannot be empty")
        if len(value) > 5000:
            raise serializers.ValidationError("Message too long (max 5000 chars)")
        return value.strip()


class ChatConversationSerializer(serializers.ModelSerializer):
    """Chat conversation serializer"""
    
    ChatApp = ChatAppSerializer(read_only=True)
    unread_count = serializers.SerializerMethodField()
    last_message_preview = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatConversation
        fields = [
            'id', 'user', 'ChatApp', 'is_active',
            'started_at', 'last_message_at', 
            'unread_count', 'last_message_preview'
        ]
        read_only_fields = ['id', 'user', 'started_at', 'last_message_at']
    
    def get_unread_count(self, obj):
        """Get unread message count"""
        return obj.get_unread_count()
    
    def get_last_message_preview(self, obj):
        """Get last message preview"""
        last_msg = obj.get_last_message()
        if last_msg:
            content = last_msg.message_content
            return content[:50] + '...' if len(content) > 50 else content
        return None


class ChatConversationCreateSerializer(serializers.ModelSerializer):
    """Create conversation serializer"""
    
    class Meta:
        model = ChatConversation
        fields = ['ChatApp']
    
    def validate_ChatApp(self, value):
        if value and not value.is_active:
            raise serializers.ValidationError("ChatApp is not active")
        return value