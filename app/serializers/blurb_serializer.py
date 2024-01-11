from rest_framework.serializers import ModelSerializer

from app.models import Blurb, BlurbList, BlurbListItem


class BlurbListItemSerializer(ModelSerializer):
    class Meta:
        model = BlurbListItem
        fields = ['id', 'text', 'order']


class BlurbListSerializer(ModelSerializer):
    items = BlurbListItemSerializer(many=True)

    class Meta:
        model = BlurbList
        fields = ['id', 'type', 'items']


class BlurbSerializer(ModelSerializer):
    lists = BlurbListSerializer(many=True)

    class Meta:
        model = Blurb
        fields = ['id', 'heading', 'body', 'order', 'lists']
        depth = 2
