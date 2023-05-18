import matplotlib
import matplotlib.pyplot as plt
import pandas

# Подготовка данных для построения графика
data = pandas.read_csv("statistics.csv")

print(data.head())


plt.plot(data["user"], data["status"])
plt.show()

plt.savefig("plot.png")
