import secrets
import string

from db import get_source, insert_click, insert_resource

def generate_base62_7():
    alphabet = string.digits + string.ascii_letters
    return ''.join(secrets.choice(alphabet) for _ in range(7))

def save_resource(source):
    alias = generate_base62_7()

    result = insert_resource(alias, source)
    return result[1]

def show_source(alias):
    result = get_source(alias)
    if result == None:
        return result
    return result[0], result[1]

def save_click(alias_id):
    result = insert_click(alias_id)
    return result[1]