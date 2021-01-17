from uuid import uuid4

__all__ = ['inc', 'dec', 'generate_hash']

def inc(i):
	return i + 1

def dec(i):
	return i - 1

def generate_hash():
    return uuid4().hex
