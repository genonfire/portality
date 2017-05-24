from rest_framework import serializers
from issue.models import Issue

class IssueSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50, required=False)
    subject = serializers.CharField(max_length=100)
    url = serializers.CharField(max_length=255)
    archive = serializers.BooleanField(required=False)
    datetime = serializers.DateTimeField(required=False)
    count = serializers.IntegerField(default=1)
    claimusers = serializers.CharField(required=False)

    def create(self, validated_data):
        new_email = validated_data.get('email')
        claimusers = validated_data.get('claimusers')
        if new_email:
            issue, created = Issue.objects.get_or_create(
            url=validated_data.get('url', None),
            defaults={'url': validated_data.get('url', None),
                'subject': validated_data.get('subject', None),
                'email': validated_data.get('email', None),
                'claimusers': validated_data.get('claimusers', None),
                'count': 1
            })
        else:
            issue, created = Issue.objects.get_or_create(
            url=validated_data.get('url', None),
            defaults={'url': validated_data.get('url', None),
                'subject': validated_data.get('subject', None),
                'claimusers': validated_data.get('claimusers', None),
                'count': 1
            })
        if not created:
            existusers = issue.claimusers.split(',')
            if claimusers not in existusers:
                issue.claimusers += "," + claimusers
                issue.count = issue.count + 1
            if new_email and not issue.email:
                issue.email = new_email
            issue.save()

        return issue
