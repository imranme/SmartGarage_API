from django.db import models
from django.conf import settings

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
        return self.name


class ChatConversation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_conversations'
    )
    ChatApp = models.ForeignKey(
        ChatApp,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations'
    )
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_conversations'
        ordering = ['-last_message_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['-last_message_at']),
        ]

    def __str__(self):
        app_name = self.ChatApp.name if self.ChatApp else "Unknown"
        return f"{self.user.email} - {app_name}"

    def get_unread_count(self):
        return self.messages.filter(
            is_read=False
        ).exclude(sender=self.user).count()

    def get_last_message(self):
        return self.messages.order_by('-sent_at').first()


class ChatMessage(models.Model):
    SENDER_TYPE_CHOICES = [
        ('user', 'User'),
        ('ChatApp', 'ChatApp'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_content = models.TextField()
    sender_type = models.CharField(max_length=20, choices=SENDER_TYPE_CHOICES, default='user')
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['conversation', 'sent_at']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.sender.email} - {self.sent_at.strftime('%Y-%m-%d %H:%M')}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
