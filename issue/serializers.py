from rest_framework import serializers
from issue.models import Issue

class IssueSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    subject = serializers.CharField(max_length=100)
    url = serializers.CharField(max_length=255)
    archive = serializers.BooleanField(required=False)
    datetime = serializers.DateTimeField(required=False)
    count = serializers.IntegerField(default=1)

    def create(self, validated_data):
        issue, created = Issue.objects.get_or_create(
        url=validated_data.get('url', None),
        defaults={'url': validated_data.get('url', None),
            'subject': validated_data.get('subject', None),
            'email': validated_data.get('email', None),
            'count': 1
        })
        if not created:
            issue.count = issue.count + 1
            issue.save()
        return issue
