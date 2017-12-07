import logging

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_api.authentication import HasPermission
from rest_framework.response import Response
from rest_framework.status import *


from accounts.models import Alert
logger = logging.getLogger(__name__)

@api_view(['POST'])
def send_station_match_alert(request):
    permission_classes = (IsAuthenticated, HasPermission)
    permissions_required = []
    Alert.objects.send_alert('Station Trafficker Match',
        context={"matched_by": request.user,
                "candidate": request.data['candidate']})
    return Response({"message": "Match Alert Sent!"}, HTTP_200_OK)