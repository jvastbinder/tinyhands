import logging

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dataentry.helpers import related_items_helper
from dataentry.models import Address1
from dataentry.models import Address2
from dataentry.serializers import Address2Serializer, Address2RelatedItemsSerializer, Address1Serializer, Address1RelatedItemsSerializer
from rest_api.authentication import HasPermission

logger = logging.getLogger(__name__)


class Address2ViewSet(viewsets.ModelViewSet):
    queryset = Address2.objects.all().select_related('address1', 'canonical_name__address1')
    serializer_class = Address2Serializer
    permission_classes = (IsAuthenticated, HasPermission)
    permissions_required = ['permission_address2_manage']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name', 'address1__name', 'longitude', 'latitude', 'level', 'verified', 'canonical_name__name')
    ordering = ('name',)

    @detail_route()
    def related_items(self, request, pk):
        try:
            address = Address2.objects.get(pk=pk)
        except:
            logger.error('Could not find Address2 with the following id: ' + pk)
            return Response({'detail': "Address2 not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Address2RelatedItemsSerializer(address)
        return Response(serializer.data)

    def there_are_no_related_items(self, address):
        count = 0
        for related_items_and_ids in related_items_helper(self, address):
            count += len(related_items_and_ids['ids'])
        if count > 0:
            return False
        return True

    def destroy(self, request, pk, *args, **kwargs):
        try:
            address = Address2.objects.get(pk=pk)
        except:
            logger.error('Could not find Address2 with the following id: ' + pk)
            return Response({'detail' : "Address2 not found"}, status=status.HTTP_404_NOT_FOUND)

        if self.there_are_no_related_items(address):
            return super(Address2ViewSet, self).destroy(request, args, kwargs)
        else:
            logger.debug('Address2 could not be deleted due to related items on the following address1: ' + pk)
            return Response({'detail': "This Address 2 could not be deleted because it is being used by other resources"}, status=status.HTTP_409_CONFLICT)


class Address1ViewSet(viewsets.ModelViewSet):
    queryset = Address1.objects.all()
    serializer_class = Address1Serializer
    permission_classes = (IsAuthenticated, HasPermission)
    permissions_required = ['permission_address2_manage']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name', 'longitude', 'latitude', 'level', 'completed')
    ordering = ('name',)

    @list_route()
    def list_all(self, request):
        address1s = Address1.objects.all()
        serializer = self.get_serializer(address1s, many=True)
        return Response(serializer.data)

    @detail_route()
    def related_items(self, request, pk):
        try:
            address = Address1.objects.get(pk=pk)
        except:
            logger.error('Could not find Address1 with the following id: ' + pk)
            return Response({'detail': "Address1 not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = Address1RelatedItemsSerializer(address)
        return Response(serializer.data)

    def there_are_no_related_items(self, address):
        count = 0
        for related_items_and_ids in related_items_helper(self, address):
            count += len(related_items_and_ids['ids'])
        if count > 0:
            return False
        return True

    def destroy(self, request, pk, *args, **kwargs):
        try:
            address = Address1.objects.get(pk=pk)
        except:
            logger.error('Could not find Address1 with the following id: ' + pk)
            return Response({'detail': "Address1 not found"}, status=status.HTTP_404_NOT_FOUND)

        if self.there_are_no_related_items(address):
            return super(Address1ViewSet, self).destroy(request, args, kwargs)
        else:
            logger.debug('Address1 could not be deleted due to related items on the following address1: ' + pk)
            return Response({'detail': "This Address 1 could not be deleted because it is being used by other resources"}, status=status.HTTP_409_CONFLICT)