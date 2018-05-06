import sys
sys.path.append('../src/api')

import nutrition

n = nutrition.Nutrition()
myFoods = [
    {'quantity': 2, 'name': 'apple'},
    {'quantity': 1, 'name': 'pizza slice'}
]
print n.getCalories(myFoods)