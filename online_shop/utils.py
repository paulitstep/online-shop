import random
import string


def random_string_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
    order_id_new = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id_new).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return order_id_new


def unique_key_generator(instance):
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_order_id_generator(instance)
    return key
