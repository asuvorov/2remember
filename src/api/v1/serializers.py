"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.contrib.auth import authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers

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
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

            return obj.full_name

    def get_value(self, obj):
        """Get Value."""
        try:
            return f"{obj.full_name} | {obj.address.short_address}"
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

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
