from rest_framework import serializers

from .models import Crawler


class CrawlerSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()

    class Meta:
        model = Crawler
        exclude = ('cancel_flag',)
