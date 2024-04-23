import random
from django.utils.text import slugify

def random_integer_generator(size=5, min_value=0, max_value=99999):
    return random.randint(min_value, max_value)

def unique_quotation_id_generator(instance, new_slug=None):
    
    q_new_id = random_integer_generator()
    
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(q_id=q_new_id).exists()

    if qs_exists:
        return unique_quotation_id_generator(instance)
    return q_new_id
