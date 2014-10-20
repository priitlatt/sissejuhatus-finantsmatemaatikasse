
# coding: utf-8

# In[1]:

import datetime

import numpy as np
import matplotlib.pyplot as plt


# In[2]:

data = []

# loeme andmed sisse

with open('tallink.csv') as f:
    header_string = next(f)
    for line in f:
        data.append(line.strip().split(','))

headers = {k.strip().lower(): i for i, k in 
           enumerate(header_string.split(','))}


# In[3]:

# koostame andmete põhjal kuupäevade ja hindade järjendid

dates = []
for line in data:
    date_string = line[headers['date']]
    date = datetime.date(*reversed(map(int, date_string.split('.'))))
    dates.append(date)

prices = np.array(
    map(float, (line[headers['open price']] for line in data))
)

# alghinnaks määrame viimase teadaoleva hinna
S0 = prices[-1]

# arvutame aktsiahinna muutude põhjal müü
changes_in_percentage = np.array(
    map(float, (line[headers['price change(%)']][:-1] for line in data))
)
mu = np.average(changes_in_percentage)/100

# leiame aktsiahinna muutused päevade lõikes
changes = prices[:-1] - prices[1:]


# In[4]:

plt.figure(figsize=(20, 14))
plt.rcParams['font.size'] = 16

plt.figure(1)

plt.subplot(211)
plt.xlabel('Aeg')
plt.ylabel('Hind (EUR)')
plt.title('Tallink Grupp aktsia hind')
plt.plot(dates, prices)

plt.subplot(212)
plt.xlabel('Aeg')
plt.ylabel('Muutus (EUR)')
plt.title('Tallink Grupp aktsiahinna muutused')
plt.plot(dates[1:], changes)

plt.show()


# In[9]:

# leiame muutuste põhjal standardhälbe
sigma = np.std(changes)

# defineerime simulatsioonide arvu
N = 10

plt.figure(figsize=(20, 12))
plt.rcParams['font.size'] = 20

plt.xlabel('Aeg')
plt.ylabel('Hind (EUR)')
plt.title('Tallink Grupp aktsiahinna simulatsioon')

simulations = []

# teostame simulatsioonid ning kanname tulemused graafikule
for i in range(N):
    rand = np.random.randn(1, len(prices))[0]
    dS = sigma*prices*rand + mu*prices
    S = S0 + dS
    simulations.append(S)
    plt.plot(S, label="Simulatsioon nr %d" % (i+1))

plt.legend(loc='best')
plt.show()


# In[10]:

rows = int(N/2) + N % 2
columns = 2

plt.figure(figsize=(16, rows*4))
plt.rcParams['font.size'] = 10

plt.figure(1)
for i, S in enumerate(simulations):
    plt.subplot(rows, columns, i+1)
    plt.title("Simulatsioon %d" % (i+1))
    plt.plot(S)
plt.show()


# In[ ]:



