from exceptions import ParasiteDisconnected

def connected(f):
    def wrapper(*args):
        if f.connected():
            return f(*args)
        else:
            raise ParasiteDisconnected
    return wrapper

# def connected(f):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             if f.connected():
#                 return func(*args, **kwargs)
#             else:
#                 raise ParasiteDisconnected
#         return wrapper
#     return decorator