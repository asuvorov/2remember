"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.db import connection

from ddcore.Decorators import exception
from ddcore.Utilities import (
    escape_html,
    escape_string)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ HELPERS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@exception
def insert_seo_model_instance_metadata(
        path, title, description, keywords, heading, object_id, content_type_id):
    """Insert SEO Model Instance Metadata."""
    with connection.cursor() as cursor:
        query = """
            INSERT INTO
                djangoseo_metadatamodelinstance
            (
                title,
                description,
                keywords,
                heading,
                _path,
                _object_id,
                _content_type_id
            )
            VALUES
            (
                '{title}',
                '{description}',
                '{keywords}',
                '{heading}',
                '{path}',
                {object_id},
                {content_type_id}
            );
        """.format(
            title=escape_string(
                escape_html(title[:60])),
            description=escape_string(
                escape_html(description[:150])),
            keywords=escape_string(
                escape_html(keywords)),
            heading=escape_string(
                escape_html(heading)),
            path=escape_string(
                escape_html(path)),
            object_id=object_id,
            content_type_id=content_type_id,
        )

        cursor.execute(query)

        if cursor.rowcount > 0:
            return True

    return False


@exception
def update_seo_model_instance_metadata(
        path, title, description, keywords, heading, object_id, content_type_id):
    """Update SEO Model Instance Metadata."""
    with connection.cursor() as cursor:
        query = """
            UPDATE
                djangoseo_metadatamodelinstance
            SET
                title='{title}',
                description='{description}',
                keywords='{keywords}',
                heading='{heading}'
            WHERE
                _object_id = {object_id} AND
                _content_type_id = {content_type_id};
        """.format(
            title=escape_string(
                escape_html(title[:60])),
            description=escape_string(
                escape_html(description[:150])),
            keywords=escape_string(
                escape_html(keywords)),
            heading=escape_string(
                escape_html(heading)),
            object_id=object_id,
            content_type_id=content_type_id,
        )

        cursor.execute(query)

        if cursor.rowcount > 0:
            return True

        return insert_seo_model_instance_metadata(
            path=path,
            title=title,
            description=description,
            keywords=keywords,
            heading=heading,
            object_id=object_id,
            content_type_id=content_type_id)

    return False
