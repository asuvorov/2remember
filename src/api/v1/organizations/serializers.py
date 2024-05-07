"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

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
