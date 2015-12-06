import matplotlib.pyplot as plt

raw_data = []
with open('run.txt') as f:
    for line in f:
        raw_data.append(line.split(","))

data = []
for line in raw_data:
    try:
        data.append([float(item) for item in line])
    except ValueError:
        pass

fs = [line[1] for line in data]
fc = [line[2] for line in data]
fr = [line[3] for line in data]

plt.plot(fs[:2000], 'r-')
plt.plot(fc[:2000], 'y-')
plt.plot(fr[:2000], 'b-')
plt.show()
