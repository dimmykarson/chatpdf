import random

def random_code():
    codigo = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return codigo