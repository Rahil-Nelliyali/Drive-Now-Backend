from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Room, Message
from .serializer import RoomSerializer, MessageSerializer


class RoomListView(APIView):
    def get(self, request):
        renter_id = self.request.query_params.get("renter")
        rooms = Room.objects.filter(renter=renter_id)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllRoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class RoomDetailView(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = RoomSerializer(room)
        return Response(serializer.data)


class MessageListView(APIView):
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND
            )
        messages = room.messages.all()

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = MessageSerializer(data=request.data)
        print(serializer.is_valid())
        print(serializer.errors)
        if serializer.is_valid():
            message = serializer.save(room=room)
            return Response(
                MessageSerializer(message).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageDetailView(APIView):
    def get(self, request, room_id, message_id):
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return Response(
                {"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND
            )
        try:
            message = room.messages.get(id=message_id)
        except Message.DoesNotExist:
            return Response(
                {"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = MessageSerializer(message)
        return Response(serializer.data)


class RoomCreateAPIView(APIView):
    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
