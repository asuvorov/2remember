"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from rest_framework import serializers

from organizations.models import (
    Organization,
    OrganizationGroup)


class AutocompleteOrganizationSerializer(serializers.HyperlinkedModelSerializer):
    """Organization Serializer."""

    class Meta:
        """Docstring."""

        model = Organization
        fields = (
            "id",
            "organization_id",
            "name",
            "description")


class OrganizationGroupSerializer(serializers.HyperlinkedModelSerializer):
    """Organization Group Serializer."""

    class Meta:
        """Docstring."""

        model = OrganizationGroup
        fields = (
            "id",
            "organization_id",
            "name",
            "description")
