from rest_framework import viewsets, serializers
from .models import Essay, Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FilesSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

class PostViewSet(viewsets.ModelViewSet):

    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    filter_backends = [SearchFilter]
    search_fields = ('title', 'body')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    #현재 request를 보낸 유저 = self.request.user

    def get_queryset(self):
        qs = super().get_queryset()

        if self.request.user.is_authenticated:
            if self.request.user.username == 'admin':
                qs = qs.all()
            else:
                qs = qs.filter(author=self.request.user)
        else:
            qs = qs.none()
        return qs

class ImgViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer

    #parser_class 지정
    parser_classes = (MultiPartParser, FormParser)
    
    #create() 오버라이딩
    #API HTTP -> get(), post() HTTP메소드에 따라서 오버라이딩 시켰지
    
    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, stats=HTTP_201_CREATED)
        else:
            return Response(serializer.error, status=HTTP_400_BAD_REQUEST)