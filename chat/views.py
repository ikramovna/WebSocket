from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import User, Message
from .serializers import MessageSerializer


class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return Message.objects.none()  # Return an empty queryset for unauthenticated users
        # Filter messages based on the currently authenticated user
        return Message.objects.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        # Set the sender as the currently authenticated user
        serializer.save(sender=self.request.user)
