# -*- coding: utf-8 -*-

"""
Tutvustame järgnevas Pythoni lisamooduli NumPy (NUMerical PYthon,
www.numpy.org) lihtsamaid finantsalaseid meetodeid intresside arvutamiseks
või kasutamiseks.

Täpsemalt uurime meetodeid
1) fv (future value);
2) pv (present value);
3) nper (number of periodic payments);
4) rate (rate of interest per period).
"""

import numpy as np

"""
------------------------------------------------------------------------------
fv (future value) -- tulevikuväärtuse arvutamine
fv(rate, nper, pmt, pv, when='end'),
mis antud
 * hetkeväärtuse `pv`,
 * intressimäära 'rate`, mis lisandub kord perioodis,
 * perioodide arvu `nper`,
 * fikseeritud makse `pmt`,
 * maksmishekte `when` perioodi sees (vaikimisi perioodi lõpus ehk 'end',
   võimalik ka perioodi alguses 'begin')
korral tagastab
 * väärtuse, mis saadakse hetkeväärtusest pärast `nper` perioodi.

Parameetrite tüübid on:
 * rate : skalaar või järjend
   Intressimäär perioodis arvuna (mitte protsendina)
 * nper : skalaar või järjend
   Perioodide arv
 * pmt : skalaar või järjend
   Makse suurus
 * pv : skalaar või järjend
   Hetkeväärtus
 * when : string 'begin' või 'end', valikultine
   Millal makse sooritama peab (alguses või lõpus)

Näide 1
Mis on tulevikuväärtus 100€ alginvesteeringu korral 10 aasta pärast, kui
aastane intressimäär on 3.5% ning me lisame igal kuu alguses (lõpus)
investeeringule 100€?
------------------------------------------------------------------------------
"""

print("Näide 1\n-------\n")

RATE = 0.035 / 12  # 3.5% aastas, 3.5%/12 perioodis
PERIOD = 10*12  # 10 aastat
PAYMENT = -100  # maksame 100€ kuus, '-' tähendab raha väljavoolu
PRESENT_VALUE = -100  # alginvesteering 100€, '-' tähendab raha väljavoolu

FV_1 = np.fv(RATE, PERIOD, PAYMENT, PRESENT_VALUE, when='end')
FV_2 = np.fv(RATE, PERIOD, PAYMENT, PRESENT_VALUE, when='begin')

print("Kuu lõpus makstes koguneb 10 aastaga %.2f€." % FV_1)
print("Kuu alguses makstes koguneb 10 aastaga %.2f€." % FV_2)

"""
Sisestades intressimäära järjendina, saame võrrelda erinevate
määrade korral saadavaid tulemusi.
"""

RATES = np.array([0.02, 0.03, 0.035, 0.04, 0.045])
FUTURE_VALUES = np.fv(RATES/12, PERIOD, PAYMENT, PRESENT_VALUE, when='end')
for rate, fv in zip(RATES, FUTURE_VALUES):
    print("Intressimäära {0:.1f}% korral on tulevikuväärtus {1:.2f}€."
          .format(rate*100, fv)
          )

"""
------------------------------------------------------------------------------
pv (present value) -- hetkeväärtuse arvutamine
pv(rate, nper, pmt, fv=0.0, when='end'),
mis antud
 * tulevikuväärtuse `fv`,
 * intressimäära 'rate`, mis lisandub kord perioodis,
 * perioodide arvu `nper`,
 * fikseeritud makse `pmt`,
 * maksmishekte `when` perioodi sees (vaikimisi perioodi lõpus ehk 'end',
   võimalik ka perioodi alguses 'begin')
korral tagastab
 * hetkeväärtuse praegu.

Parameetrite tüübid on:
 * rate : skalaar või järjend
   Intressimäär perioodis arvuna (mitte protsendina)
 * nper : skalaar või järjend
   Perioodide arv
 * pmt : skalaar või järjend
   Makse suurus
 * fv : skalaar või järjend, valikuline
   Tulevikuväärtus
 * when : string 'begin' või 'end', valikultine
   Millal makse sooritama peab (alguses või lõpus)

Näide 2
Kui suur peab olema investeeringu hetkeväärtus, et 10 aasta päras oleks
kogunenud 14485.09€, kui aastane intressimäär on 3.5% ning me lisame
investeeringule iga kuu 100€? Kui suur peab olema alginvesteering, et selline
summa koguneks 5, 6, 7, 8 või 9 aastaga?
------------------------------------------------------------------------------
"""

print("\nNäide 2\n-------\n")

RATE = 0.035 / 12  # 3.5% aastas, 3.5%/12 perioodis
PERIOD = 10*12  # 10 aastat
PAYMENT = -100  # maksame 100€ kuus, '-' tähendab raha väljavoolu
FV = 14485.09  # soovitud tulemus

PRESENT_VALUE = np.pv(RATE, PERIOD, PAYMENT, FV, when='end')
print("Et toota {0}€, peaks investeeringu hetkeväärtus olema {1:.2f}€."
      .format(FV, -PRESENT_VALUE)  # '-' tähistab väljaminekut
      )

PERIODS = np.array([5, 6, 7, 8, 9])
PRESENT_VALUES = np.pv(RATE, PERIODS*12, PAYMENT, FV, when='end')
for period, pv in zip(PERIODS, PRESENT_VALUES):
    print("{0} aasta korral peaks investeeringu hetkeväärtus olema {1:.2f}€."
          .format(period, -pv)  # '-' tähistab väljaminekut
          )

"""
------------------------------------------------------------------------------
nper (net present value) -- perioodiliste maksete arvu arvutamine
nper(rate, pmt, pv, fv=0, when='end')
mis antud
 * hetkeväärtuse `pv`,
 * tulevikuväärtuse `fv`,
 * intressimäära 'rate`, mis lisandub kord perioodis,
 * fikseeritud makse `pmt`,
 * maksmishekte `when` perioodi sees (vaikimisi perioodi lõpus ehk 'end',
   võimalik ka perioodi alguses 'begin')
korral tagastab
 * vajalike maksete arvu.

Parameetrite tüübid on:
 * rate : skalaar või järjend
   Intressimäär perioodis arvuna (mitte protsendina)
 * pmt : skalaar või järjend
   Makse suurus
 * fv : skalaar või järjend, valikuline
   Tulevikuväärtus
 * pv : skalaar või järjend, valikuline
   Hetkeväärtus
 * when : string 'begin' või 'end', valikultine
   Millal makse sooritama peab (alguses või lõpus)

Näide 3
Kui laenu tagasimakse suurus on 330€ kuus, siis kui kaua kulub 68000€ suuruse
laenu maksmiseks aastase intressimäära 2.8% juures?
------------------------------------------------------------------------------
"""

print("\nNäide 3\n-------\n")

RATE = 0.03 / 12  # 4% aastas, 3.5%/12 kuus
PAYMENT = -330  # maksame 330€ kuus, '-' tähendab raha väljavoolu
PV = 68000  # laenu suurus

PERIOD_COUNT = np.nper(RATE, PAYMENT, PV)
print("{0}€ tasumiseks kulub {1:.2f} kuud ehk {2:.0f} aastat."
      .format(PV, PERIOD_COUNT, PERIOD_COUNT/12)
      )

PAYMENTS = np.arange(300, 350, 10)
PERIOD_COUNTS = np.nper(RATE, -PAYMENTS, PV)
for pmt, period in zip(PAYMENTS, PERIOD_COUNTS):
    print("{0}€ suuruse tagasimaksega kulub {1:.2f} kuud ehk {2:.0f} aastat."
          .format(pmt, period, period/12)
          )

"""
------------------------------------------------------------------------------
rate -- perioodi intressimäära arvutamine
rate(nper, pmt, pv, fv, when='end', guess=0.1, tol=1e-06, maxiter=100)
mis antud
 * perioodide arvu `nper`,
 * fikseeritud makse `pmt`,
 * hetkeväärtuse `pv`,
 * tulevikuväärtuse `fv`,
 * maksmishekte `when` perioodi sees (vaikimisi perioodi lõpus ehk 'end',
   võimalik ka perioodi alguses 'begin')
korral tagastab
 * intressimäära ühe perioodi kohta.

Parameetrite tüübid on:
 * nper : skalaar või järjend
   Perioodide arv
 * pmt : skalaar või järjend
   Makse suurus
 * fv : skalaar või järjend, valikuline
   Tulevikuväärtus
 * pv : skalaar või järjend, valikuline
   Hetkeväärtus
 * when : string 'begin' või 'end', valikultine
   Millal makse sooritama peab (alguses või lõpus)

Näide 4
Millise aastase intressimäära juures koguneb 10 aasta jooksul 15000€, kui
me hoiustame iga kuu 100€?
------------------------------------------------------------------------------
"""

print("\nNäide 4\n-------\n")

PERIOD = 10*12  # 10 aastat igakuise maksega
PAYMENT = -100  # maksame 100€ kuus, '-' tähendab raha väljavoolu
PV = 0  # laenu suurus
FV = 15000

rate = np.rate(PERIOD, PAYMENT, PV, FV)
print("{0}€ kogunemiseks peab aastane intressimäär olema {1:.2f}%."
      .format(FV, 100*12*rate))
