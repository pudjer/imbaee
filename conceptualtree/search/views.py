from rest_framework import viewsets

from backend.models import Branch
from backend.serializers import NodeSerializer
from backend.views import NodeViewSet
from search.documents import NodeDocument



class SearchNodeViewSet(NodeViewSet):
    def get_queryset(self):
        queryset = NodeDocument.search().query('match', content=str(self.kwargs['query'])).to_queryset()
        return queryset
