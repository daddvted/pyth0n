import functools


def hello(path, *, data):
    def wrapped(func):

        functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            print(f'hello, {path}, {data}')
            return func(*args, **kwargs)
        return wrapped_func
    return wrapped


def cached(key: str = ""):
    def wrapper(func):

        @functools.wraps(func)
        def wrapper_for_func(*args, **kwargs):
            # Hijack trick happens HERE
            if key:
                return key
            else:
                return func(*args, **kwargs)

        return wrapper_for_func

    return wrapper


@hello(path="dead", data="heheheh")
# cache() function with parameter will hijack output of dude()
@cached()
def dude(name: str = 'Dude'):
    print("in dude")
    return f"hey {name}"


if __name__ == "__main__":
    result = dude('sucker')
    print(result)
