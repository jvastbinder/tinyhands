from django.conf.urls import url
from rest_framework.authtoken import views

from accounts.views import AccountViewSet, DefaultPermissionsSetViewSet, CurrentUserView, ResendActivationEmailView, AccountActivateClient
from dataentry.views import Address2ViewSet, Address1ViewSet, GeoCodeAddress1APIView, GeoCodeAddress2APIView, InterceptionRecordViewSet, VictimInterviewViewSet, BatchView, IntercepteeViewSet, VictimInterviewDetailViewSet, PhotoExporter
from dataentry.views import PersonViewSet
from dataentry.views import SiteSettingsViewSet
from dataentry.views import get_station_id
from events.views import EventViewSet
from portal.views import get_interception_records, TallyDaysView
from static_border_stations.views import BorderStationViewSet, StaffViewSet, CommitteeMemberViewSet, LocationViewSet


list = {'get': 'list', 'post': 'create'}
detail = {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}

urlpatterns = [
    # Accounts App
        url(r'^login/', views.obtain_auth_token),
        url(r'^me/$', CurrentUserView.as_view(), name="CurrentUser"),

        url(r'^account/$', AccountViewSet.as_view(list), name="AccountList"),
        url(r'^account/all/$', AccountViewSet.as_view({'get': 'list_all'}), name="AccountListAll"),
        url(r'^account/(?P<pk>\d+)/$', AccountViewSet.as_view(detail), name='Account'),
        url(r'^account/activate/(?P<activation_key>[a-zA-Z0-9]+)/$', AccountActivateClient.as_view(), name='accountActivation'),
        url(r'^account/resend-activation-email/(?P<pk>\d+)/$', ResendActivationEmailView.as_view(), name='ResendActivationEmail'),

        url(r'^defaultPermissionsSet/$', DefaultPermissionsSetViewSet.as_view(list), name="DefaultPermissionsSets"),
        url(r'^defaultPermissionsSet/(?P<pk>\d+)/$', DefaultPermissionsSetViewSet.as_view(detail), name="DefaultPermissionsSet"),


    # Data Entry App
        # Addresses
        url(r'^address1/$', Address1ViewSet.as_view(list), name='Address1'),
        url(r'^address1/all/$', Address1ViewSet.as_view({'get': 'list_all'}), name='Address1all'),
        url(r'^address1/(?P<pk>\d+)/$', Address1ViewSet.as_view(detail), name='Address1detail'),
        url(r'^address1/(?P<pk>\d+)/related-items/$', Address1ViewSet.as_view({'get': 'related_items'}), name='Address1RelatedItems'),

        url(r'^address2/$', Address2ViewSet.as_view(list), name='Address2'),
        url(r'^address2/(?P<pk>\d+)/$', Address2ViewSet.as_view(detail), name='Address2detail'),
        url(r'^address2/(?P<pk>\d+)/related-items/$', Address2ViewSet.as_view({'get': 'related_items'}), name='Address2RelatedItems'),

        url(r'^address1/fuzzy/$', GeoCodeAddress1APIView.as_view(), name="Address1FuzzySearch"),
        url(r'^address2/fuzzy/$', GeoCodeAddress2APIView.as_view(), name="Address2FuzzySearch"),

        # IRFs
        url(r'^irf/$', InterceptionRecordViewSet.as_view(list), name="InterceptionRecord"),
        url(r'^irf/(?P<pk>\d+)/$', InterceptionRecordViewSet.as_view(detail), name="InterceptionRecordDetail"),

        # Interceptee
        url(r'^interceptee/$', IntercepteeViewSet.as_view(list), name="Interceptee"),
        url(r'^interceptee/(?P<pk>\d+)/$', IntercepteeViewSet.as_view(detail), name="IntercepteeDetail"),

        #SiteSettings
        url(r'^site-settings/$', SiteSettingsViewSet.as_view({'get': 'retrieve_custom'}), name="SiteSettings"),
        url(r'^site-settings/(?P<pk>\d+)/$', SiteSettingsViewSet.as_view({'put': 'update'}), name="SiteSettingsUpdate"),

        # VIFs
        url(r'^vif/$', VictimInterviewViewSet.as_view(list), name="VictimInterview"),
        url(r'^vif/(?P<pk>\d+)/$', VictimInterviewDetailViewSet.as_view(detail), name="VictimInterviewDetail"),


    # Portal App
        url(r'^get_interception_records/$', get_interception_records, name='get_interception_records'),
        url(r'^portal/tally/days/$', TallyDaysView.as_view(), name='tally_day_api'),



    # Static Border Station App
        # Border Stations
        url(r'^border-station/$', BorderStationViewSet.as_view({'get':'list_all', 'post':'create'}), name="BorderStations"), # Detail
        url(r'^border-station/(?P<pk>\d+)/$', BorderStationViewSet.as_view(detail), name="BorderStation"),
        url(r'^get_station_id/', get_station_id, name='get_station_id'),



        # Committee Members
        url(r'^committee-member/$', CommitteeMemberViewSet.as_view(list), name="CommitteeMembers"),
        url(r'^committee-member/(?P<pk>\d+)/$', CommitteeMemberViewSet.as_view(detail), name="CommitteeMember"),

        # Locations
        url(r'^location/$', LocationViewSet.as_view(list), name="Locations"),
        url(r'^location/(?P<pk>\d+)/$', LocationViewSet.as_view(detail), name="Location"),

        # Staff
        url(r'^staff/$', StaffViewSet.as_view(list), name="AllStaff"),
        url(r'^staff/(?P<pk>\d+)/$', StaffViewSet.as_view({'get': 'staff_retrieve', 'put': 'update', 'delete': 'destroy'}), name="Staff"),

        #IRFBatch
        url(r'^batch/(?P<startDate>(\d+)-(\d+)-\d+)/(?P<endDate>\d+-\d+-\d+)/$', BatchView.as_view(), name="BatchView"),
        url(r'^photos/(?P<startDate>(\d+)-(\d+)-\d+)/(?P<endDate>\d+-\d+-\d+)/$', PhotoExporter.as_view({'get': 'export_photos'}), name="PhotoExporter"),
        url(r'^photos/(?P<startDate>(\d+)-(\d+)-\d+)/(?P<endDate>\d+-\d+-\d+)/count/$', PhotoExporter.as_view({'get': 'count_photos_in_date_range'}), name="PhotoExporterCount"),

        #Persons
        url(r'^person/$', PersonViewSet.as_view({'get': 'list'}), name="Person"),
        #url(r'^person/(?P<pk>\d+)/$', IdFormMatch, name="PersonForm"),

    # Events
        url(r'^event/$', EventViewSet.as_view({'get': 'list', 'post':'create'}), name="EventList"),
        url(r'^event/(?P<pk>\d+)/$', EventViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'}), name='Event'),
        url(r'^event/all/$', EventViewSet.as_view({'get': 'list_all'}), name="EventListAll"),
        url(r'^event/feed/calendar/$', EventViewSet.as_view({'get': 'calendar_feed'}), name='EventCalendarFeed'),
        url(r'^event/feed/dashboard/$', EventViewSet.as_view({'get': 'dashboard_feed'}), name='EventDashboardFeed'),
]
