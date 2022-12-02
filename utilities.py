import random
import string

async def generate_token(id: str):
    length_of_token = 12
    identifier = ""

    for i in range(length_of_token):
        identifier += random.choice(string.ascii_letters)
    return identifier