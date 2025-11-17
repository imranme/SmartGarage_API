from django.urls import path
from .views import (
    ChatAppListCreateView,
    ChatAppDetailView,

    ConversationListCreateView,
    ConversationDetailView,
    ConversationUnreadCountView,

    MessageListCreateView,
    MarkMessagesReadView
)

app_name = "chatapp"

urlpatterns = [

    # -------------------------------
    # ChatApp CRUD
    # -------------------------------
    path('apps/', ChatAppListCreateView.as_view(), name='chatapp-list-create'),
    path('apps/<int:pk>/', ChatAppDetailView.as_view(), name='chatapp-detail'),

    # -------------------------------
    # Chat Conversation Endpoints
    # -------------------------------
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list-create'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<int:pk>/unread-count/', ConversationUnreadCountView.as_view(),
         name='conversation-unread-count'),

    # -------------------------------
    # Chat Messages Endpoints
    # -------------------------------
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/mark-read/', MarkMessagesReadView.as_view(), name='message-mark-read'),

]
