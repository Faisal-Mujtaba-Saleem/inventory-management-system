from typing import Union, TypeAlias
from inventory.models import Category, SubCategory

QueryData: TypeAlias = Union[
    list[dict],
    dict
]


def populateRelationalFields(query_data: QueryData, relational_fields: list, relational_models: list):

    if len(relational_fields) == len(relational_models):

        if isinstance(query_data, list):

            for query_dict in query_data:
                for i, relational_field in enumerate(relational_fields):
                    relational_model = relational_models[i]

                    relational_field_id = query_dict['fields'].get(
                        relational_field)
                    relational_field_obj = relational_model.objects.get(
                        pk=relational_field_id)

                    if relational_field == 'supplier':
                        query_dict['fields'][relational_field] = {
                            'id': relational_field_obj.id,
                            'name': relational_field_obj.name,
                            'email': relational_field_obj.email,
                            'phone': relational_field_obj.phone
                        }
                    else:
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

                if relational_field == 'supplier':
                    query_dict['fields'][relational_field] = {
                        'id': relational_field_obj.id,
                        'name': relational_field_obj.name,
                        'email': relational_field_obj.email,
                        'phone': relational_field_obj.phone
                    }
                else:
                    query_dict['fields'][relational_field] = {
                        'id': relational_field_obj.id,
                        'name': relational_field_obj.name,
                        'slug': relational_field_obj.slug
                    }

    else:
        raise Exception(
            'Number of relational fields does not match number of relational models')
