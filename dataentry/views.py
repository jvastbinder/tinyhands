from datetime import date
import csv
import json
import os
import re
import shutil

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, render_to_response, render
from django.template.loader import render_to_string
from django.views.generic import ListView, View, DeleteView, CreateView

from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet
from braces.views import LoginRequiredMixin
from fuzzywuzzy import process

from dataentry.models import (BorderStation, VDC, District, Interceptee, InterceptionRecord, VictimInterview, VictimInterviewLocationBox, VictimInterviewPersonBox)
from dataentry.forms import (IntercepteeForm, InterceptionRecordForm, VDCForm, DistrictForm, VictimInterviewForm, VictimInterviewLocationBoxForm, VictimInterviewPersonBoxForm)
from dataentry import csv_io
from dataentry.serializers import DistrictSerializer, VDCSerializer, InterceptionRecordListSerializer, VictimInterviewListSerializer

from accounts.mixins import PermissionsRequiredMixin

from alert_checkers import IRFAlertChecker, VIFAlertChecker
from fuzzy_matching import match_location
from rest_api.authentication import HasPermission, HasDeletePermission


@login_required
def home(request):
    return redirect("main_dashboard")


class SearchFormsMixin(object):
    # Will equal name of field to search
    Name = None
    Number = None

    def __init__(self, *args, **kw):
        for key, value in kw.iteritems():
            if value == "name":
                self.Name = key
            elif value == "number":
                self.Number = key

    def get_queryset(self):
        try:
            value = self.request.GET['search_value']
        except:
            value = ''
        if value != '':
            code = value[:3]
            stations = BorderStation.objects.filter(station_code__startswith=code)
            if len(stations) != 0:
                object_list = self.model.objects.filter(**{self.Number: value})
                if len(object_list) == 0:
                    object_list = self.model.objects.filter(**{self.Name: value})
            else:
                object_list = self.model.objects.filter(**{self.Name: value})
        else:
            object_list = self.model.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SearchFormsMixin, self).get_context_data(**kwargs)
        # Check if database is empty to change message in search page
        context['database_empty'] = self.model.objects.count() == 0
        return context


@login_required
def interception_record_list_template(request):
    return render(request, 'dataentry/interceptionrecord_list.html')

@login_required
def interception_record_list_search_template(request, code):
    station_code = code
    search = 1
    return render(request, 'dataentry/interceptionrecord_list.html', locals())


class IntercepteeInline(InlineFormSet):
    model = Interceptee
    extra = 12
    max_num = 12

    def get_factory_kwargs(self):
        kwargs = super(IntercepteeInline, self).get_factory_kwargs()
        kwargs['form'] = IntercepteeForm
        return kwargs


class IRFImageAssociationMixin(object):
    def forms_invalid(self, form, inlines):
        for name, file in self.request.FILES.iteritems():
            match = re.match(r"interceptees-(\d+)-photo", name)
            irf_num = self.request.POST.get("irf_number")

            try:
                extension = file.name.split(".")[-1]
            except Exception:
                extension = None

            if match is not None and irf_num is not None and extension is not None:
                interceptee_index = match.group(1)
                filename = "unassociated_photos/irf-photo-%s-index-%s.%s" % (irf_num, interceptee_index, extension)
                default_storage.save(filename, ContentFile(file.read()))

        return super(IRFImageAssociationMixin, self).forms_invalid(form, inlines)

    def forms_valid(self, form, inlines):
        interceptees = inlines[0]
        if not os.path.exists(settings.BASE_DIR + '/media/unassociated_photos/'):
            os.makedirs(settings.BASE_DIR + '/media/unassociated_photos/')
        image_paths = os.listdir(settings.BASE_DIR + '/media/unassociated_photos/')
        for path in image_paths:
            match = re.match(r"irf-photo-(.*)-index-(\d+)\.(.*)", path)
            if match is not None:
                irf_number = match.group(1)
                interceptee_index = int(match.group(2))
                full_image_path = settings.BASE_DIR + '/media/unassociated_photos/' + path
                dest_image_path = settings.BASE_DIR + '/media/interceptee_photos/' + path
                if form.instance.irf_number != irf_number:
                    continue
                try:
                    interceptee = interceptees[interceptee_index]
                    shutil.move(full_image_path, dest_image_path)
                    interceptee.instance.photo = dest_image_path
                except IndexError:
                    continue
        return super(IRFImageAssociationMixin, self).forms_valid(form, inlines)


class InterceptionRecordCreateView(LoginRequiredMixin, PermissionsRequiredMixin, IRFImageAssociationMixin, CreateWithInlinesView):
    model = InterceptionRecord
    form_class = InterceptionRecordForm
    success_url = reverse_lazy('interceptionrecord_list')
    inlines = [IntercepteeInline]
    permissions_required = ['permission_irf_add']

    def forms_valid(self, form, inlines):
        form.instance.form_entered_by = self.request.user
        form.instance.date_form_received = date.today()
        form = form.save()
        for formset in inlines:
            formset.save()
        IRFAlertChecker(form, inlines).check_them()
        return HttpResponseRedirect(self.get_success_url())


class InterceptionRecordUpdateView(LoginRequiredMixin, PermissionsRequiredMixin, IRFImageAssociationMixin, UpdateWithInlinesView):
    model = InterceptionRecord
    form_class = InterceptionRecordForm
    success_url = reverse_lazy('interceptionrecord_list')
    inlines = [IntercepteeInline]
    permissions_required = ['permission_irf_edit']

    def forms_valid(self, form, inlines):
        form = form.save()
        for formset in inlines:
            formset.save()
        IRFAlertChecker(form, inlines).check_them()
        return HttpResponseRedirect(self.get_success_url())


class InterceptionRecordDetailView(InterceptionRecordUpdateView):
    permissions_required = ['permission_irf_view']

    def post(self, request, *args, **kwargs):
        raise PermissionDenied


class PersonBoxInline(InlineFormSet):
    model = VictimInterviewPersonBox
    extra = 12

    def get_factory_kwargs(self):
        kwargs = super(PersonBoxInline, self).get_factory_kwargs()
        kwargs['form'] = VictimInterviewPersonBoxForm
        return kwargs


class LocationBoxInline(InlineFormSet):
    model = VictimInterviewLocationBox
    extra = 8

    def get_factory_kwargs(self):
        kwargs = super(LocationBoxInline, self).get_factory_kwargs()
        kwargs['form'] = VictimInterviewLocationBoxForm
        return kwargs


class VictimInterviewListView(LoginRequiredMixin, SearchFormsMixin, ListView):
    model = VictimInterview

    def __init__(self, *args, **kwargs):
        # Passes what to search by to SearchFormsMixin
        super(VictimInterviewListView, self).__init__(vif_number__icontains="number", interviewer__icontains="name")


@login_required
def victiminterview_record_list_search_template(request, code):
    station_code = code
    search = 1
    return render(request, 'dataentry/victiminterview_list.html', locals())


class VictimInterviewCreateView(LoginRequiredMixin, PermissionsRequiredMixin, CreateWithInlinesView):
    model = VictimInterview
    form_class = VictimInterviewForm
    success_url = reverse_lazy('victiminterview_list')
    inlines = [PersonBoxInline, LocationBoxInline]
    permissions_required = ['permission_vif_add']

    def forms_valid(self, form, inlines):
        form.instance.form_entered_by = self.request.user
        form.instance.date_form_received = date.today()
        form = form.save()
        for formset in inlines:
            formset.save()
        VIFAlertChecker(form, inlines).check_them()
        return HttpResponseRedirect(self.get_success_url())


class VictimInterviewUpdateView(LoginRequiredMixin, PermissionsRequiredMixin, UpdateWithInlinesView):
    model = VictimInterview
    form_class = VictimInterviewForm
    success_url = reverse_lazy('victiminterview_list')
    inlines = [PersonBoxInline, LocationBoxInline]
    permissions_required = ['permission_vif_edit']

    def forms_valid(self, form, inlines):
        form = form.save()
        for formset in inlines:
            formset.save()
        VIFAlertChecker(form, inlines).check_them()
        return HttpResponseRedirect(self.get_success_url())


class VictimInterviewDetailView(VictimInterviewUpdateView):
    permissions_required = ['permission_vif_view']

    def post(self, request, *args, **kwargs):
        raise PermissionDenied


class InterceptionRecordCSVExportView(LoginRequiredMixin, PermissionsRequiredMixin, View):
    permissions_required = ['permission_irf_view']

    def get(self, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        today = date.today()
        response['Content-Disposition'] = 'attachment; filename=irf-all-data-%d-%d-%d.csv' % (today.year, today.month, today.day)

        writer = csv.writer(response)
        irfs = InterceptionRecord.objects.all()
        csv_rows = csv_io.get_irf_export_rows(irfs)
        writer.writerows(csv_rows)

        return response


class VictimInterviewCSVExportView(LoginRequiredMixin, PermissionsRequiredMixin, View):
    permissions_required = ['permission_vif_view']

    def get(self, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        today = date.today()
        response['Content-Disposition'] = 'attachment; filename=vif-all-data-%d-%d-%d.csv' % (today.year, today.month, today.day)

        writer = csv.writer(response)
        vifs = VictimInterview.objects.select_related('person_boxes').select_related('location_boxes').all()
        csv_rows = csv_io.get_vif_export_rows(vifs)
        writer.writerows(csv_rows)

        return response


class GeoCodeDistrictAPIView(APIView):
    def get(self, request):
        value = request.query_params['district']
        matches = match_location(district_name=value)
        if matches:
            serializer = DistrictSerializer(matches, many=True)
            return Response(serializer.data)
        else:
            return Response({"id": "-1", "name": "None"})


class GeoCodeVdcAPIView(APIView):
    def get(self, request):
        try:
            district_name = request.query_params['district']

        except:
            district_name = None
        vdc_name = request.query_params['vdc']
        matches = match_location(district_name, vdc_name)
        if matches:
            serializer = VDCSerializer(matches, many=True)
            return Response(serializer.data)
        else:
            return Response({"id": "-1", "name": "None"})


class VDCAdminView(LoginRequiredMixin, PermissionsRequiredMixin, SearchFormsMixin, ListView):
    model = VDC
    template_name = "dataentry/vdc_admin_page.html"
    permissions_required = ['permission_vdc_manage']
    paginate_by = 25

    def __init__(self, *args, **kwargs):
        super(VDCAdminView, self).__init__(name__icontains="name")

    def get_queryset(self):
        return self.model.objects.all().select_related('district', 'canonical_name__district')

    def get_context_data(self, **kwargs):
        context = super(VDCAdminView, self).get_context_data(**kwargs)
        context['search_url'] = '/data-entry/geocodelocations/vdc-admin/search/'
        context['database_empty'] = self.model.objects.count() == 0
        return context


class VDCSearchView(LoginRequiredMixin, PermissionsRequiredMixin, SearchFormsMixin, ListView):
    model = VDC
    template_name = "dataentry/vdc_admin_page.html"
    permissions_required = ['permission_vdc_manage']
    paginate_by = 25

    def get(self, request, value, *args, **kwargs):
        self.object_list = self.get_queryset(value)
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(("Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})
        context = self.get_context_data()
        return self.render_to_response(context)

    def __init__(self, *args, **kwargs):
        super(VDCSearchView, self).__init__(name__icontains="name")

    def get_queryset(self, searchValue):
        return self.model.objects.filter(name__contains=searchValue).select_related('district', 'canonical_name__district')

    def get_context_data(self, **kwargs):
        context = super(VDCSearchView, self).get_context_data(**kwargs)
        context['search_url'] = '/data-entry/geocodelocations/vdc-admin/search/'
        context['database_empty'] = self.model.objects.count() == 0
        return context


class VDCCreateView(LoginRequiredMixin, PermissionsRequiredMixin, CreateView):
    model = VDC
    form_class = VDCForm
    template_name = "dataentry/vdc_create_page.html"
    permissions_required = ['permission_vif_add', 'permission_irf_add']

    def form_valid(self, form):
        form.save()
        return HttpResponse(render_to_string('dataentry/vdc_create_success.html'))


class DistrictAdminView(LoginRequiredMixin, PermissionsRequiredMixin, SearchFormsMixin, ListView):
    model = District
    template_name = "dataentry/district_admin_page.html"
    permissions_required = ['permission_vdc_manage']

    def __init__(self, *args, **kwargs):
        super(DistrictAdminView, self).__init__(name__icontains="name")

    def get_context_data(self, **kwargs):
        context = super(DistrictAdminView, self).get_context_data(**kwargs)
        context['database_empty'] = self.model.objects.count() == 0
        return context


class DistrictCreateView(LoginRequiredMixin, PermissionsRequiredMixin, CreateView):
    model = District
    form_class = DistrictForm
    template_name = "dataentry/district_create_page.html"
    permissions_required = ['permission_vif_add', 'permission_irf_add']

    def form_valid(self, form):
        form.save()
        return HttpResponse(render_to_string('dataentry/district_create_success.html'))


class StationCodeAPIView(APIView):
    def get(self, request):
        codes = BorderStation.objects.all().values_list("station_code", flat=True)
        return Response(codes, status=status.HTTP_200_OK)


@login_required
def interceptee_fuzzy_matching(request):
    input_name = request.GET['name']
    all_people = Interceptee.objects.all()
    people_dict = {serializers.serialize("json", [obj]): obj.full_name for obj in all_people }
    matches = process.extractBests(input_name, people_dict, limit=10)
    return HttpResponse(json.dumps(matches), content_type="application/json")


def get_station_id(request):
    code = request.GET['code']
    if code == '':
        return HttpResponse([-1])
    else:
        station = BorderStation.objects.filter(station_code=code)
        if len(station) > 0:
            print("Station id is: " + str(station))
            return HttpResponse([station[0].id])
        else:
            print("No station id")
            return HttpResponse([-1])


class Address2ViewSet(viewsets.ModelViewSet):
    queryset = VDC.objects.all().select_related('district', 'canonical_name__district')
    serializer_class = VDCSerializer
    permission_classes = (IsAuthenticated, HasPermission)
    permissions_required = ['permission_vdc_manage']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name', 'district__name', 'longitude', 'latitude', 'verified', 'canonical_name__name')
    ordering = ('name',)


class Address1ViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = (IsAuthenticated, HasPermission)
    permissions_required = ['permission_vdc_manage']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('name',)
    ordering_fields = ('name',)
    ordering = ('name',)

    @list_route()
    def list_all(self, request):
        districts = District.objects.all()
        serializer = self.get_serializer(districts, many=True)
        return Response(serializer.data)


class InterceptionRecordViewSet(viewsets.ModelViewSet):
    queryset = InterceptionRecord.objects.all()
    serializer_class = InterceptionRecordListSerializer
    permission_classes = (IsAuthenticated, HasPermission, HasDeletePermission,)
    permissions_required = ['permission_irf_view']
    delete_permissions_required = ['permission_irf_delete']

    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('irf_number',)
    ordering_fields = ('irf_number', 'staff_name', 'number_of_victims', 'number_of_traffickers', 'date_time_of_interception', 'date_time_entered_into_system', 'date_time_last_updated',)
    ordering = ('irf_number',)


class VictimInterviewViewSet(viewsets.ModelViewSet):
    queryset = VictimInterview.objects.all()
    serializer_class = VictimInterviewListSerializer
    permission_classes = (IsAuthenticated, HasPermission, HasDeletePermission,)
    permissions_required = ['permission_vif_view']
    delete_permissions_required = ['permission_vif_delete']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = ('vif_number',)
    ordering_fields = ('vif_number', 'interviewer', 'number_of_victims', 'number_of_traffickers', 'date', 'date_time_entered_into_system', 'date_time_last_updated',)
    ordering = ('vif_number',)

