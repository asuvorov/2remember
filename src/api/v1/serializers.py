"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers
from termcolor import cprint

from ddcore.models.Address import Address
from ddcore.models.Phone import Phone

# pylint: disable=import-error
from accounts.models import UserProfile


# -----------------------------------------------------------------------------
# --- Authorization.
# -----------------------------------------------------------------------------
class AuthTokenSerializer(serializers.Serializer):
    """Auth Token Serializer."""

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        """Validate."""
        username = attrs.get("username").lower()
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                username=username,
                password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError(_("User Account is disabled."))

                attrs["user"] = user

                return attrs

            raise serializers.ValidationError(_("Unable to login with provided Credentials."))

        raise serializers.ValidationError(_("Must include \"username\" and \"password\""))


# -----------------------------------------------------------------------------
# --- Autocomplete.
# -----------------------------------------------------------------------------
class AutocompleteMemberSerializer(serializers.HyperlinkedModelSerializer):
    """Autocomplete Member Serializer."""

    uuid = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "uuid",
            "label",
            "value",
            "avatar",
        )

    def get_uuid(self, obj):
        """Get User ID."""
        return obj.user_id

    def get_label(self, obj):
        """Get Label."""
        try:
            return f"{obj.full_name} | {obj.address.short_address}"
        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

            return obj.full_name

    def get_value(self, obj):
        """Get Value."""
        try:
            return f"{obj.full_name} | {obj.address.short_address}"
        except Exception as exc:
            cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                   f"                 {type(exc).__name__}\n"
                   f"                 {str(exc)}", "white", "on_red")

            return obj.full_name


# -----------------------------------------------------------------------------
# --- Core
# -----------------------------------------------------------------------------
class AddressSerializer(serializers.HyperlinkedModelSerializer):
    """Address Serializer."""

    class Meta:
        model = Address
        fields = (
            "address_1",
            "address_2",
            "city",
            "zip_code",
            "province",
            "country",
        )


class PhoneSerializer(serializers.HyperlinkedModelSerializer):
    """Phone Number Serializer."""

    class Meta:
        model = Phone
        fields = (
            "phone_number",
            "mobile_phone_number",
        )
