import threading

from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Crawler
from .serializers import CrawlerSerializer

from .crawler import run


class CrawlerList(generics.ListCreateAPIView):
    queryset = Crawler.objects.all()
    serializer_class = CrawlerSerializer
    permission_classes = (IsAdminUser, )

    def perform_create(self, serializer):
        crawler = serializer.save(status='creating')
        thread = threading.Thread(target=run, args=(crawler,))
        thread.start()


class CrawlerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Crawler.objects.all()
    serializer_class = CrawlerSerializer
    permission_classes = (IsAdminUser, )

    def perform_update(self, serializer):
        serializer.save(cancel_flag=True)
