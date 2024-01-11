from rest_framework.serializers import ModelSerializer

from app.models import Job


class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'description', 'location', 'contract_type']
        depth = 1
