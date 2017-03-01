import StringIO

from braces.views import LoginRequiredMixin
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from lxml import etree
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from templated_email import send_templated_mail
from z3c.rml import document

from accounts.mixins import PermissionsRequiredMixin
from budget.models import BorderStationBudgetCalculation, StaffSalary
from dataentry.models import BorderStation
from budget.helpers import MoneyDistributionFormHelper
from rest_api.authentication import HasPermission
from static_border_stations.models import Staff, CommitteeMember
from static_border_stations.serializers import StaffSerializer, CommitteeMemberSerializer


class MoneyDistribution(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, HasPermission]
    permissions_required = ['permission_budget_view']

    def retrieve(self, request, pk):
        border_station = BorderStationBudgetCalculation.objects.get(pk=pk).border_station
        staff = border_station.staff_set.all().exclude(email__isnull=True)
        committee_members = border_station.committeemember_set.all().exclude(email__isnull=True)

        staff_serializer = StaffSerializer(staff, many=True)
        committee_members_serializer = CommitteeMemberSerializer(committee_members, many=True)

        pdf_url = settings.SITE_DOMAIN + reverse('MdfPdf', kwargs={"pk": pk})

        return Response({"staff_members": staff_serializer.data, "committee_members": committee_members_serializer.data, "pdf_url": pdf_url})

    def send_emails(self, request, pk):
        staff_ids = request.data['staff_ids']
        budget_calc_id = pk
        committee_ids = request.data['committee_ids']

        budget_calc = BorderStationBudgetCalculation.objects.get(pk=budget_calc_id)
        border_station = BorderStation.objects.get(pk=budget_calc.border_station.id)

        staff = border_station.staff_set.all()
        committee_members = border_station.committeemember_set.all()

        # Go through all people associated with station, save their settings and send email if selected
        for person in staff:
            if person.id in staff_ids:
                if person.receives_money_distribution_form == False:
                    person.receives_money_distribution_form = True
                    person.save()
                self.email_staff_and_committee_members(person, budget_calc_id, 'money_distribution_form')
            else:
                person.receives_money_distribution_form = False
                person.save()

        for person in committee_members:
            if person.id in committee_ids:
                if person.receives_money_distribution_form == False:
                    person.receives_money_distribution_form = True
                    person.save()
                self.email_staff_and_committee_members(person, budget_calc_id, 'money_distribution_form')
            else:
                person.receives_money_distribution_form = False
                person.save()
        return Response("Emails Sent!", status=200)

    def email_staff_and_committee_members(self, person, budget_calc_id, template, context={}):
        context['person'] = person
        context['budget_calc_id'] = budget_calc_id
        context['site'] = settings.SITE_DOMAIN
        send_templated_mail(
            template_name=template,
            from_email=settings.ADMIN_EMAIL_SENDER,
            recipient_list=[person.email],
            context=context
        )


class PDFView(View, LoginRequiredMixin, PermissionsRequiredMixin):
    permissions_required = ['permission_budget_view']
    filename = 'report.pdf'
    template_name = ''

    def get_filename(self):
        return self.filename

    def get_context_data(self):
        return {}

    def dispatch(self, request, *args, **kwargs):
        if self.template_name == '':
            raise ImproperlyConfigured(
                "A template_name must be specified for the rml template.")

        # Use StringIO and not cStringIO because cStringIO can't accept unicode characters
        buf = StringIO.StringIO()
        rml = render_to_string(self.template_name, self.get_context_data())

        self.rml = render_to_string(self.template_name, self.get_context_data())

        buf.write(rml)
        buf.seek(0)
        root = etree.parse(buf).getroot()
        doc = document.Document(root)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = "filename=%s" % self.get_filename()
        response['X-Frame-Options'] = "*"

        doc.process(response)
        return response


class MoneyDistributionFormPDFView(PDFView, LoginRequiredMixin, PermissionsRequiredMixin):
    permissions_required = ['permission_budget_view']
    template_name = 'budget/MoneyDistributionTemplateV2.rml'
    filename = 'Monthly-Money-Distribution-Form.pdf'

    def get_context_data(self):
        budget_id = self.kwargs['pk']
        mdf_helper = MoneyDistributionFormHelper(budget_id)
        return {
            'name': mdf_helper.station_name,
            'date': mdf_helper.date_entered,
            'sections': mdf_helper.sections,
            'total': mdf_helper.total
        }
