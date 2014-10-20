# coding: utf-8

# MTMM.00.195 Sissejuhatus finantsmatemaatikasse
# 2. kodutöö - Priit Lätt

# Impordime edaspidises vajaminevad moodulid:
#  * `datetime` - kuupäevade formaatimiseks,
#  * `numpy` - vektorarvutuse jaoks,
#  * `matplotlib` - jooniste tegemiseks,
#  * `HTML` - algandmete tabelina kuvamiseks.

import datetime

from IPython.display import HTML
import numpy as np
import matplotlib.pyplot as plt

# Loeme algandmed sisse failist `tallink.csv` ning salvestame nad listi `data`.

data = []

with open('tallink.csv') as f:
    header_string = next(f)
    for line in f:
        data.append(line.strip().split(','))

headers = {k.strip().lower(): i for i, k in
           enumerate(header_string.split(','))}

# Kuvame algandmed `HTML` tabelina.

table = "<table>{headers}{rows}</table>"
table_headers, table_rows = "", ""

for header in header_string.split(','):
    table_headers += "<th>{}</th>".format(header)

for row in data:
    columns = map(lambda v: "<td>{}</td>".format(v), row)
    table_rows += "<tr>{}</tr>".format(''.join(columns))

HTML(table.format(headers=table_headers, rows=table_rows))

# Koostame andmete põhjal kuupäevade järjendi `dates`
# ja hindade järjendi `prices`.

dates = []
for line in data:
    date_string = line[headers['date']]
    date = datetime.date(*reversed(map(int, date_string.split('.'))))
    dates.append(date)

prices = np.array(
    map(float, (line[headers['open price']] for line in data))
)

# Määrame alghinnaks `S0` viimase teadaoleva hinna.

S0 = prices[-1]

# Arvutame aktsiahinna muutude põhjal $\mu$ ja salvestame
# selle muutujasse `mu`.

changes_in_percentage = np.array(
    map(float, (line[headers['price change(%)']][:-1] for line in data))
)
mu = np.average(changes_in_percentage) / 100

# Leiame aktsiahinna muutused päevade lõikes ja salvestame nad
# järjendisse `changes`.

changes = prices[:-1] - prices[1:]

# Joonestame algandmed graafikule. Esimesel graafikul on toodud
# **Tallinki** aktsia hind ning teisel aktsiahinna muutused päevade lõikes.

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

# Leiame muutuste põhjal standardhälbe $\Sigma$ ning salvestame ta
# muutujasse `sigma` ning defineerime simulatsioonide arvu `n = 10`.

sigma = np.std(changes)
N = 10

# Teostame simulatsioonid ja salvestame nad järjendisse `simulations`.

simulations = []

for i in range(N):
    rand = np.random.randn(1, len(prices))[0]
    dS = sigma*prices*rand + mu*prices
    S = [S0]
    for ds in dS:
        S.append(S[-1] + ds)
    simulations.append(S)

# Kanname simulatsioonide tulemused ühele graafikule.

plt.figure(figsize=(20, 12))
plt.rcParams['font.size'] = 20

plt.xlabel('Aeg')
plt.ylabel('Hind (EUR)')
plt.title('Tallink Grupp aktsiahinna simulatsioon')

for i, sim in enumerate(simulations):
    plt.plot(sim, label="Simulatsioon nr %d" % (i+1))

plt.legend(loc='best')
plt.show()

# Joonestame selguse mõttes simulatsioonid välja ka eraldi teljestikes.

rows = int(N/2) + N % 2
columns = 2

plt.figure(figsize=(16, rows*3))
plt.rcParams['font.size'] = 8

plt.figure(1)
for i, S in enumerate(simulations):
    plt.subplot(rows, columns, i+1)
    plt.title("Simulatsioon %d" % (i+1))
    plt.plot(S)
plt.show()
