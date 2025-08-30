from rest_framework import serializers

from study.models import StudyModel


class StudySerializer(serializers.ModelSerializer):
    # 모델에 author FK가 있으면 author.username을, 없으면 None을 반환하도록 안전 처리
    # username = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = StudyModel
        fields = ('pk', 'name', 'description', 'username', 'created_at')
        read_only_fields = ('created_at', 'updated_at')

    def get_username(self, obj):
        author = getattr(obj, 'auther', None)
        return getattr(author, 'username', None)