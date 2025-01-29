from django.urls import path
from rest_framework_nested import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'chats', ChatViewSet, basename="chats")

chats_router = routers.NestedDefaultRouter(router, 'chats', lookup='chat')   
chats_router.register('messages', ChatMessageViewSet, basename='chat-messages')

urlpatterns = router.urls + chats_router.urls