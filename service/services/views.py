from django.db.models import F, Sum
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().select_related('plan', 'client', 'client__user').only(
        'client__user__email',
        'client__company_name',
        'plan_id',
        'price',
    )
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)

        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        response.data = response_data

        return response