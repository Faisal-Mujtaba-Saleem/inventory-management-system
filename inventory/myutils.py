from inventory.models import Category, SubCategory


def poulateRelatedFields(querylist=None, related_field=None, related_model=None):
    for query_dict in querylist:
        related_field_id = query_dict['fields'].get(related_field)
        related_field_obj = related_model.objects.get(pk=related_field_id)

        query_dict['fields'][related_field] = {
            'id': related_field_obj.id,
            'name': related_field_obj.name,
            'slug': related_field_obj.slug
        }

    if querylist is not None and querylist[0]['model'] == 'inventory.item' and related_field == 'category':
        poulateRelatedFields(querylist, 'sub_category', SubCategory)
