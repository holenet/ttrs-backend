from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('crawlers/', views.CrawlerList.as_view()),
    path('crawlers/<int:pk>/', views.CrawlerDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
