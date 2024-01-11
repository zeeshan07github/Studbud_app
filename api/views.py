from rest_framework.decorators import api_view
from rest_framework.response import Response
from studbud.models import room
from .serializers import roomserializer
@api_view(['GET'])
def get_routes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id ',
    ]
    return Response(routes)

# @api_view(['GET'])
# def get_room(request):
#     rooms = room.objects.all()
#     return Response(rooms)

@api_view(['GET'])
def get_rooms(request):
    rooms = room.objects.all()
    serializer = roomserializer(rooms , many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_room(request , pk):
    rooms = room.objects.get(id=pk)
    serializer = roomserializer(rooms , many=False)
    return Response(serializer.data)