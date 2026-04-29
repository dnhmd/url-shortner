import secrets
import string

from db import get_source, insert_resource

def save_resource(source):
    alias = generate_base62_7()

    result = insert_resource(alias, source)
    return result[1]

def show_source(alias):
    result = get_source(alias)
    if result == None:
        return result
    return result[0]

def generate_base62_7():
    alphabet = string.digits + string.ascii_letters
    return ''.join(secrets.choice(alphabet) for _ in range(7))