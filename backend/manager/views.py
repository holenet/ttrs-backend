import threading

from django.apps import apps
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser

from .models import Crawler
from .serializers import CrawlerSerializer, CrawlerDetailSerializer, TableSerializer

from .crawler import run

@api_view(['GET'])
@permission_classes((IsAdminUser,))
def count_tables(request):
    """
    List # of instances for each table(model)
    """
    print(apps.get_models())
    # serializer = CountTablesSerializer(many=True)
    # print(serializer.data)

# @api_view(['GET', 'POST'])
# @permission_classes((IA))
# def delete_tables(request):
#     """
#     List # of instances for each table(model)
#     Or delete all instances for each table at once.
#     """
#     if request.method == 'GET':
#         counts = {}



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
    serializer_class = CrawlerDetailSerializer
    permission_classes = (IsAdminUser, )

    def perform_update(self, serializer):
        serializer.save(cancel_flag=True)
