from rest_framework.serializers import ModelSerializer


def hateoasLink(permission):
    def deco(orgFunction):
        def newFunc(*args, **kwargs):
            return orgFunction(*args, **kwargs)
        return newFunc
    return deco


class HateoasModelSerializer(ModelSerializer):
    def to_representation(self, instance):
        rep = super(HateoasModelSerializer, self).to_representation(instance)
        model = instance
        user = self.context['request'].user
        rep['_links'] =
        return rep

    def _get_links(self):
        link_methods = [getattr(self, x) for x in dir(self) if x.startswith('link_')]
        method_results = [x() for x in link_methods]
        return method_results




class HateoasLink:

    # Figure out how permissions work
    # Create basic permission link
    # Assign link classes to meta classes
    # class decorator instead of inheritance?

    def __init__(self, link_description, link_url, permission_group, permission_action, ):
        self.link_description = link_description
        self.link_url = link_url
        self.permission_group = permission_group
        self.permission_action = permission_action

    def get_link(self, model, user):
        if self.has_permission(model, self.permission_action, user):
            return self.link_description, self.link_url
        else:
            return None

    def has_permission(self, model, permission_action, user):
        return False


class UserLocationHateoasLink(HateoasLink):

