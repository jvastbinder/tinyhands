from django.conf.urls import patterns, url

from dataentry.views import Address2ViewSet, Address1ViewSet, GeoCodeDistrictAPIView, GeoCodeVdcAPIView
from budget.views import BudgetViewSet, OtherItemsViewSet

urlpatterns = patterns('rest_api.views',
    # Budget URLs
    url(r'^budgetcalculationform/$', BudgetViewSet.as_view({'get': 'list', 'post': 'create'}), name='BudgetCalculation'),
    url(r'^budgetcalculationform/(?P<pk>\d+)/$', BudgetViewSet.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}), name='BudgetCalculationWithId'),

    # Other items
    url(r'^budgetcalculationform/(?P<parent_pk>\d+)/otheritem/$', OtherItemsViewSet.as_view({'get': 'list_by_budget_sheet', 'post': 'create'}), name='BudgetCalculationWithId'),
    url(r'^budgetcalculationform/(?P<parent_pk>\d+)/otheritem/(?P<pk>\d+)/$', OtherItemsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='BudgetCalculationWithId'),


    # Addresses
    url(r'^address1/$', Address1ViewSet.as_view({'get': 'list', 'post': 'create'}), name='Address1'),
    url(r'^address1/all/$', Address1ViewSet.as_view({'get': 'list_all', 'post': 'create'}), name='Address1'),
    url(r'^address1/(?P<pk>\d+)/$', Address1ViewSet.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}), name='Address1detail'),

    url(r'^address2/$', Address2ViewSet.as_view({'get': 'list', 'post': 'create'}), name='Address2'),
    url(r'^address2/(?P<pk>\d+)/$', Address2ViewSet.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}), name='Address2detail'),

    # Fuzzy searching for addresses
    url(r'^address1/fuzzy/$', GeoCodeDistrictAPIView.as_view()),
    url(r'^address2/fuzzy/$', GeoCodeVdcAPIView.as_view()),
)
