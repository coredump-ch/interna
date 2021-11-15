from rest_framework.views import APIView
from rest_framework.response import Response

from . import models


def serialize_date(val):
    return val.isoformat() if val else None


def serialize_category(val):
    try:
        return models.Membership.CATEGORY[val]
    except KeyError:
        return 'Unknown'


class ActiveMemberView(APIView):
    def get(self, request, format=None):
        """
        Return active members as JSON response.
        """
        memberships = models.Membership.active.order_by('Member__id')
        data = [{
            'member': {
                'id': m.Member.id,
                'name': m.Member.name,
                'email': m.Member.email,
            },
            'membership': {
                'start': serialize_date(m.start),
                'end': serialize_date(m.end),
                'category': {
                    'id': m.category,
                    'description': serialize_category(m.category),
                },
            },
        } for m in memberships]
        return Response(data)
