import threading

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Crawler
from .serializers import CrawlerSerializer

from .crawler import run


class CrawlerList(generics.ListCreateAPIView):
    queryset = Crawler.objects.all()
    serializer_class = CrawlerSerializer
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        crawler = serializer.save(status='creating')
        thread = threading.Thread(target=run, args=(crawler,))
        thread.start()
