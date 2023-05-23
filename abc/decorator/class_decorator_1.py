class MyDecorator:
    # target function passed in __init__()
    def __init__(self, f):
        print("inside MyDecorator.__init__()")
        f()  # Prove that function definition has completed

    def __call__(self, name='shit'):
        print(f"inside MyDecorator.__call__(), arg={name}")


@MyDecorator
def func():
    print("inside Function()")

func()
