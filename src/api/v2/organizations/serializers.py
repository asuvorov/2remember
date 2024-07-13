"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from rest_framework import serializers

from organizations.models import OrganizationGroup


class OrganizationGroupSerializer(serializers.HyperlinkedModelSerializer):
    """Organization Group Serializer."""

    class Meta:
        """Docstring."""

        model = OrganizationGroup
        fields = (
            "id",
            "organization_id",
            "name",
            "description",
        )
