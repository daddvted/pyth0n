# Functions Are Objects
# =====================
def yell(text):
    return text.upper() + '!'

print(yell('hello'))

bark = yell
print(bark('woof'))

# >>> del yell
# >>> yell('hello?')
# NameError: name 'yell' is not defined
# >>> bark('hey')
# HEY

print(bark.__name__)


# Functions Can Be Stored In Data Structures
# ==========================================
funcs = [bark, str.lower, str.capitalize]
print(funcs)
for f in funcs:
    print(f, f("hi there"))

print(funcs[0]("yo man"))


# Functions Can Be Passed To Other Functions
# ==========================================
def greet(func):
    greeting = func("Hi, I'm Python")
    print(greeting)
greet(yell)

def whisper(text):
    return text.lower() + '...'

greet(whisper)
print(map(yell, ['Hi', 'Hey', 'hi']))



# Functions Can Be Nested
# =======================
def speak(text):
    def whisper(t):
        return t.lower() + '...'
    return whisper(text)

print(speak("hi man"))

# >>> whisper('Yo')
# NameError: "name 'whisper' is not defined"
# 
# >>> speak.whisper
# AttributeError: "'function' object has no attribute 'whisper'"


def get_speak_func(volume):
    def whisper(text):
        return text.lower() + '...'
    def yell(text):
        return text.upper() + '!'
    if volume > 0.5:
        return yell
    else:
        return whisper

print(get_speak_func(0.3))
print(get_speak_func(0.6))

speak_func = get_speak_func(0.8)
print(speak_func("oooooooooh"))



# Functions Can Capture Local State
# =================================
def get_speak_func2(text, volume):
    def whisper():
        return text.lower() + '...'
    def yell():
        return text.upper() + '!'

    if volume > 0.5:
        return yell
    else:
        return whisper

print(get_speak_func2("bitch", 0.9)())


def make_adder(n):
    def add(x):
        return x + n
    return add

plus_3 = make_adder(3)
plus_5 = make_adder(5)

print(plus_3(4))
print(plus_5(4))


# Objects Can Behave Like Functions
# =================================
class Adder:
    def __init__(self, n):
        self.n = n
    def __call__(self, x):
        return self.n + x

plus_3 = Adder(3)

print(plus_3(7))

