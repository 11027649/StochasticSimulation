import random

print("time")
for i in range(1,10):
   print(random.expovariate(15))

print("\n timeline")
t= 0
for i in range(1,10):
   t+= random.expovariate(15)
   print(t)