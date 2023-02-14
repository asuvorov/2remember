"""Define Serializers."""

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
