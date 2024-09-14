from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser

# Create your views here.
from .models import Post
from .serilizers import PostSerializer

@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser , JSONParser])
def post_api_view(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # propagate the channels
            channels_layer = get_channel_layer()
            async_to_sync(channels_layer.group_send)(
                'chat',
                {
                    'type':'chat_message',
                    'message': serializer.data
                }
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
