import json

with open('car.json', 'r') as f:
    cars = json.load(f)
    for car in cars:
#        print(car['brand'])
        print('{}: {}'.format(car['brand'], car['num']))

