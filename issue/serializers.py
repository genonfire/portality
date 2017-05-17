from rest_framework import serializers
from issue.models import Issue

class IssueSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50)
    subject = serializers.CharField(max_length=100)
    url = serializers.CharField(max_length=255)
    archive = serializers.BooleanField(required=False)
    datetime = serializers.DateTimeField()
    count = serializers.IntegerField(default=0)

    def create(self, validated_data):
        issue, created = Issue.objects.get_or_create(
        url=validated_data.get('url', None),
        defaults={'url': validated_data.get('url', None)})
        if not created:
            issue.count = issue.count + 1
            print "id: %d count: %d" % (issue.id, issue.count)
            issue.save()
            return issue
        return Issue.objects.create(**validated_data)
