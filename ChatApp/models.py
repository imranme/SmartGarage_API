from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class ChatApp(models.Model):

    name = models.CharField(max_length=255, verbose_name="ChatApp Name")
    address = models.TextField(verbose_name="Full Address")
    city = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ChatApp'
        verbose_name = 'ChatApp'
        verbose_name_plural = 'ChatApps'
        ordering = ['name']
    
    def __str__(self):
class ChatConversation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # আপনার User model
        on_delete=models.CASCADE,
        related_name='chat_conversations',
        verbose_name="User"
    )
    ChatApp = models.ForeignKey(
        ChatApp,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations',
        verbose_name="ChatApp"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Started At")
    last_message_at = models.DateTimeField(auto_now=True, verbose_name="Last Message At")
    
    class Meta:
        db_table = 'chat_conversations'
        verbose_name = 'Chat Conversation'
        verbose_name_plural = 'Chat Conversations'
        ordering = ['-last_message_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['-last_message_at']),
        ]
    
    def __str__(self):
        ChatApp_name = self.ChatApp.name if self.ChatApp else "Unknown"
        return f"{self.user.email} - {ChatAppp_name}"
    
    def get_unread_count(self):
        """Get unread message count for user"""
        return self.messages.filter(
            is_read=False
        ).exclude(sender=self.user).count()
    
    def get_last_message(self):
        """Get last message"""
        return self.messages.order_by('-sent_at').first()



class ChatMessage(models.Model):
    """
    Individual chat message
    """
    SENDER_TYPE_CHOICES = [
        ('user', 'User'),
        ('ChatApp', 'ChatApp'),
        ('system', 'System'),
    ]
    
    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="Conversation"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name="Sender"
    )
    message_content = models.TextField(verbose_name="Message")
    sender_type = models.CharField(
        max_length=20,
        choices=SENDER_TYPE_CHOICES,
        default='user',
        verbose_name="Sender Type"
    )
    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Sent At")
    
    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['conversation', 'sent_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.sender.email} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"
    
    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])