from rest_framework import serializers

from .models import Crawler


class CountTablesSerializer(serializers.Serializer):
    table_name = serializers.CharField(max_length=20)
    count = serializers.IntegerField()


class CrawlerSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    semester = serializers.ChoiceField(choices=['1학기', '여름학기', '2학기', '겨울학기'])

    class Meta:
        model = Crawler
        exclude = ('cancel_flag',)


class CrawlerDetailSerializer(CrawlerSerializer):
    year = serializers.ReadOnlyField()
    semester = serializers.ReadOnlyField()
