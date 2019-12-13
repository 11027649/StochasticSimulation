import math
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

max_temperature = 50
min_temperature = 0.1

steps = 10000

plt.figure(figsize=(8,6))
plt.title("Cooling schemes", size=25)
plt.xlabel("Steps", size=18)
plt.ylabel("Temperature", size=18)
plt.xticks(size=13)
plt.yticks(size=13)

# prepare a list with the temperatures
cooling_per_step = (max_temperature - min_temperature)/steps
temperatures = [max_temperature - cooling_per_step * step for step in range(steps)]

plt.plot(range(len(temperatures)), temperatures, label="linear", color="red")

temperatures = [max_temperature * math.exp(-0.001*x) for x in range(steps)]
plt.plot(range(len(temperatures)), temperatures, label="exponential", color="purple")

temperatures = [max_temperature * math.exp(-0.02*x) for x in range(steps)]
plt.plot(range(len(temperatures)), temperatures, label="exponential fast", color="black")

# cool twice as fast and reheat halfway through the simulation
cooling_per_step = (max_temperature - min_temperature)/(0.5 * steps)
temperatures = [max_temperature - cooling_per_step * step for step in range(int(0.5*steps))]

# second half same coolscheme
temperatures.extend(temperatures)
plt.plot(range(len(temperatures)), temperatures, label="reheat", color="green")

legend = plt.legend(prop={'size': 15})

plt.savefig("temperatures.svg", format="svg")