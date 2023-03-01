from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import *

class TagField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        queryset = self.get_queryset()
        try:
            if isinstance(data, bool):
                raise TypeError
            model = queryset.model
            return model.objects.get_or_create(pk=data)[0]
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)




class NodeSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    tags = TagField(queryset=Tag.objects.all(), many=True)
    language = TagField(queryset=Language.objects.all())
    links = serializers.SlugRelatedField(queryset=Branch.objects.all(), many=True, slug_field="slug")

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('links', 'tags').select_related('language', 'author')
        return queryset

    class Meta:
        fields = '__all__'
        model = Branch


class BranchSerializer(NodeSerializer):
    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        if obj in self.context.get('seen_branches', []):
            return 'Уже есть'
        else:
            seen_branches = self.context.get('seen_branches', []) + [obj]
            queryset = super().setup_eager_loading(obj.links.all())
            serializer = BranchSerializer(
                queryset,
                many=True, context={'seen_branches': seen_branches}
            )
            return serializer.data

    # add other fields as needed
