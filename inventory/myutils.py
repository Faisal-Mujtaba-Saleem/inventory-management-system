from typing import Union
from inventory.models import Category, SubCategory


def populateRelationalFields(query_data: Union[list[dict], dict], relational_fields: list, relational_models: list):
    if len(relational_fields) == len(relational_models):

        if isinstance(query_data, list):

            for query_dict in query_data:
                for i, relational_field in enumerate(relational_fields):
                    relational_model = relational_models[i]

                    relational_field_id = query_dict['fields'].get(
                        relational_field)
                    relational_field_obj = relational_model.objects.get(
                        pk=relational_field_id)

                    query_dict['fields'][relational_field] = {
                        'id': relational_field_obj.id,
                        'name': relational_field_obj.name,
                        'slug': relational_field_obj.slug
                    }

        elif isinstance(query_data, dict):
            query_dict = query_data

            for i, relational_field in enumerate(relational_fields):
                relational_model = relational_models[i]

                relational_field_id = query_dict['fields'].get(
                    relational_field
                )
                relational_field_obj = relational_model.objects.get(
                    pk=relational_field_id
                )

                query_dict['fields'][relational_field] = {
                    'id': relational_field_obj.id,
                    'name': relational_field_obj.name,
                    'slug': relational_field_obj.slug
                }

    else:
        raise Exception(
            'Number of relational fields does not match number of relational models')
