from rest_framework import viewsets
from revenue.models import Revenue
from revenue.api.serializers import RevenueSerializer
from core.permissions import IsCurrentVerifiedUser
from revenue.api.filters import RevenueFilterSet

class RevenueView(viewsets.ModelViewSet):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer
    permission_classes = (IsCurrentVerifiedUser,)
    filterset_class = RevenueFilterSet

    """
    Filter objects by owner
    """
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Revenue.objects.none()  # return empty queryset
        return Revenue.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        if serializer.validated_data.get('quantity'):
            self.request.user.balance += \
                serializer.validated_data.get('quantity')
            self.request.user.save()
        # Inject owner data to the serializer
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data.get('quantity'):
            self.request.user.balance += \
                serializer.validated_data.get('quantity') \
                - serializer.instance.quantity
            self.request.user.save()
        serializer.save()

    def perform_destroy(self, instance):
        self.request.user.balance -= instance.quantity
        self.request.user.save()
        instance.delete()