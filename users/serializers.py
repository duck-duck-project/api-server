from rest_framework import serializers

from users.models import User

__all__ = (
    'UserPartialSerializer',
    'ThemeSerializer',
    'UserSerializer',
    'ContactSerializer',
    'UserPartialWithThemeSerializer',
    'UserPartialWithProfilePhotoSerializer',
    'UserPartialWithCanReceiveNotificationsSerializer',
)


class ThemeSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    secret_message_template_text = serializers.CharField()
    secret_media_template_text = serializers.CharField()
    secret_message_view_button_text = serializers.CharField()
    secret_message_delete_button_text = serializers.CharField()
    secret_message_read_confirmation_text = serializers.CharField()
    secret_message_deleted_confirmation_text = serializers.CharField()
    secret_message_deleted_text = serializers.CharField()
    secret_message_missing_text = serializers.CharField()
    created_at = serializers.DateTimeField()


class UserPartialSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(allow_null=True)
    fullname = serializers.CharField()


class UserPartialWithProfilePhotoSerializer(UserPartialSerializer):
    profile_photo_url = serializers.URLField(allow_null=True)


class UserPartialWithThemeSerializer(UserPartialSerializer):
    theme = ThemeSerializer(allow_null=True)


class UserPartialWithCanReceiveNotificationsSerializer(UserPartialSerializer):
    can_receive_notifications = serializers.BooleanField()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fullname = serializers.CharField()
    username = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()
    can_be_added_to_contacts = serializers.BooleanField()
    profile_photo_url = serializers.URLField(allow_null=True)
    is_banned = serializers.BooleanField()
    can_receive_notifications = serializers.BooleanField()
    theme = ThemeSerializer(allow_null=True)
    is_blocked_bot = serializers.BooleanField()
    personality_type = serializers.CharField(allow_null=True)
    born_on = serializers.DateField(allow_null=True)
    real_first_name = serializers.CharField(allow_null=True)
    real_last_name = serializers.CharField(allow_null=True)
    patronymic = serializers.CharField(allow_null=True)
    gender = serializers.ChoiceField(
        choices=User.Gender.choices,
        allow_null=True,
    )
    nationality = serializers.CharField(
        allow_null=True,
        source='nationality.name',
    )
    region = serializers.CharField(
        allow_null=True,
        source='region.name',
    )
    country = serializers.CharField(
        allow_null=True,
        source='region.country.name',
    )
    country_flag_emoji = serializers.CharField(
        allow_null=True,
        source='region.country.flag_emoji',
    )
    contacts_sorting_strategy = serializers.ChoiceField(
        choices=User.ContactsSortingStrategy.choices,
        required=False,
    )
    is_contacts_sorting_reversed = serializers.BooleanField(required=False)
    energy = serializers.IntegerField()
    health = serializers.IntegerField()
    did_sports_at = serializers.DateTimeField(allow_null=True)
    is_premium = serializers.BooleanField()


class ContactSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserPartialWithProfilePhotoSerializer()
    public_name = serializers.CharField()
    private_name = serializers.CharField()
    is_hidden = serializers.BooleanField()
    theme = ThemeSerializer(allow_null=True)
    created_at = serializers.DateTimeField()
