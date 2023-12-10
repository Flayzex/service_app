from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subscription, Client
from .serializers import SubscriptionSerializer


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().select_related('plan', 'client', 'client__user').only(
        'client__user__email',
        'client__company_name',
        'plan_id',
    )
    serializer_class = SubscriptionSerializer