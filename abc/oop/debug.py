from test.hello import say_hello

from test.demo import KnowAll

say_hello("Shit")
print(__name__)


kw1 = KnowAll(10)
kw2 = KnowAll(10)

print(kw1.count, kw1.cls_count)
print(kw2.count, kw2.cls_count)

KnowAll.cls_count = 100
kw1.count = 99

print(kw1.count, kw1.cls_count)
print(kw2.count, kw2.cls_count)


print(kw1.__dict__)
kw1.apple = "red"

print(kw1.__dict__)
