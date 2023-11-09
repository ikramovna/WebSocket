from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User, Message
from .serializers import MessageSerializer


class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Message.objects.none()
        return Message.objects.filter(receiver=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['sender'] = request.user.id
        return super().create(request, *args, **kwargs)
