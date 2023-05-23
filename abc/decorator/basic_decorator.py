def fake(f):
    # Code written here will be executed when using "@xxx"
    # print("faked")

    def wrapper():
        print("faked")
        f()

    return wrapper


@fake
def do_real_thing():
    print("doing something")


do_real_thing()
