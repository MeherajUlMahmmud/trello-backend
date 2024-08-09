from rest_framework.serializers import ModelSerializer

from common.models import ContactUsModel


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUsModel
        ref_name = 'ContactUsSerializer'
        fields = [
            'name',
            'email',
            'message',
        ]
