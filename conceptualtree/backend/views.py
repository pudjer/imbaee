
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *



class NodeViewSet(viewsets.ModelViewSet):
    serializer_class = NodeSerializer
    queryset = Branch.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Set up eager loading to avoid N+1 selects
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    @action(methods=['GET'], detail=True)
    def show_branch(self, request, slug):
        branch = Branch.objects.get(slug=slug)
        serializer = BranchSerializer(instance=branch)
        return Response(serializer.data)
