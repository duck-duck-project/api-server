from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from secret_messages.models import Contact, SecretMessage

__all__ = (
    'ContactApi',
    'SecretMessageCreateApi',
    'SecretMessageRetrieveApi',
)


class UserContactListApi(ListAPIView):

    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = Contact
            fields = '__all__'
            depth = 1

    serializer_class = Serializer
    queryset = Contact.objects.all()
    lookup_field = 'of_user_id'
    lookup_url_kwarg = 'user_id'

    def filter_queryset(self, queryset: QuerySet[Contact]):
        return queryset.filter(of_user_id=self.kwargs['user_id'])


class ContactApi(ModelViewSet):

    class Serializer(serializers.ModelSerializer):

        class Meta:
            model = Contact
            fields = '__all__'

    serializer_class = Serializer
    queryset = Contact.objects.all()

    def perform_create(self, serializer: Serializer):
        serialized_data = serializer.validated_data
        if serialized_data['of_user'] == serialized_data['to_user']:
            raise ValidationError('User can not be contact for itself')
        super().perform_create(serializer)


class SecretMessageCreateApi(CreateAPIView):

    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = SecretMessage
            fields = '__all__'

    serializer_class = Serializer
    queryset = SecretMessage.objects.all()


class SecretMessageRetrieveApi(RetrieveAPIView):

    class Serializer(serializers.ModelSerializer):
        class Meta:
            model = SecretMessage
            fields = '__all__'
            depth = 2

    serializer_class = Serializer
    queryset = SecretMessage.objects.all()
