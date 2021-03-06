from fuzzywuzzy import process
from itertools import chain

from dataentry.models import Address1, Address2, SiteSettings, Person, Interceptee, VictimInterview


def match_location(address1_name=None, address2_name=None):
    """
    Currently we only send one, the other, or both, so that's all this function
    handles. For more flexible (and unDRY) code (which should DRYed before use),
    look at commit 656d770fbaf28c82fca7fed11e7c1679982de3a5.
    """
    filter_by_address1 = False

    # Determine the appropriate model
    if address2_name is not None and address1_name is not None:
        model = Address2
        location_name = address2_name
        filter_by_address1 = True
    elif address2_name is not None:
        model = Address2
        location_name = address2_name
    else:
        model = Address1
        location_name = address1_name

    site_settings = SiteSettings.objects.all()[0]

    if filter_by_address1:
        fuzzy_cutoff = site_settings.get_setting_value_by_name('address2_cutoff')
        fuzzy_limit = site_settings.get_setting_value_by_name('address2_limit')
        region_names = {region.id: region.name
                        for region in model.objects.filter(address1__name__contains=address1_name).select_related('address1', 'canonical_name__address1')
                        }
    else:
        fuzzy_limit = site_settings.get_setting_value_by_name('address1_limit')
        fuzzy_cutoff = site_settings.get_setting_value_by_name('address1_cutoff')
        region_names = {region.id: region.name
                        for region in model.objects.all()
                        }

    # matches is in the form of [(u'match', score, id), ...]
    matches = process.extractBests(location_name, region_names, score_cutoff=fuzzy_cutoff, limit=fuzzy_limit)

    objects = None
    if len(matches) > 0:
        objects = [model.objects.get(pk=pk) for name, score, pk in matches]
    return objects


# This function is not used anywhere else in code
def match_address2_address1(address2_name, address1_name):
    locations = [address2.name+", "+address2.address1.name for address2 in Address2.objects.all()]
    name = address2_name + ", " + address1_name
    matches = process.extractBests(name, locations, score_cutoff=70, limit=5)
    if len(matches) > 0:
        names = matches[0][0].split(", ")
        address2 = Address2.objects.get(name=names[0])
        address1 = address2.address1
        return address2, address1
    else:
        return None

def match_person(person_name, excludes):
    fuzzy_limit = 11
    fuzzy_score_cutoff=80
    victim_ids = []
    if excludes != None and excludes == 'victims':
        irf_victim_ids = Interceptee.objects.filter(kind = 'v').values_list('person', flat=True)
        vif_victim_ids = VictimInterview.objects.all().values_list('victim', flat=True)
        victim_ids = list(chain(irf_victim_ids, vif_victim_ids))
    try:
         site_settings = SiteSettings.objects.all()[0]
         fuzzy_score_cutoff = site_settings.get_setting_value_by_name('idmanagement_name_cutoff')
         fuzzy_limit = site_settings.get_setting_value_by_name('idmanagement_name_limit')
    except BaseException:
        # use default hard coded values
        pass

    results = []
    choices = {choice.id: choice.full_name
               for choice in Person.objects.all().exclude(id__in = victim_ids)
               }
    matches = process.extractBests(person_name, choices, score_cutoff=fuzzy_score_cutoff, limit=fuzzy_limit)

    for match in matches:
        results.append(Person.objects.get(id=match[2]))

    return results
