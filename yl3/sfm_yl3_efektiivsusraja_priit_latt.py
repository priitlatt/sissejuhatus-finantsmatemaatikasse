# coding: utf-8

# MTMM.00.195 Sissejuhatus finantsmatemaatikasse
# 3. kodutöö (efektiivsusraja) - Priit Lätt
#
# Lahendus toetub artiklile "Regression techniques for Portfolio
# Optimisation using MOSEK" (http://arxiv.org/abs/1310.3397) ja
# selle artikli tarbeks loodud moodulile "mosekTools"
# (https://github.com/tschm/MosekRegression).

# Sooritame vajaminevad impordid:
# * `matplotlib` graafikute joonestamiseks,
# * `numpy` andmete töötlemiseks,
# * `pandas` statistilise analüüsi tegemiseks,
# * `mosek` ja `mosektools` moodulitest vajalikud tööriistad
#    efektiivsusraja leidmiseks.

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

from mosek.fusion import Expr

import mosekTools.solver.model.model as mosek_model
import mosekTools.solver.model.math as mosek_math
import mosekTools.solver.model.bound as mosek_bound


# Loeme algandmed sisse failist `data.csv` kasutades moodulit
# pandas (http://pandas.pydata.org/) ja salvestame nad muutujasse `data`.
# Aktsiate hinnad salvestame eraldi muutujasse `stocks`.
#
# Kasutame moodulit `pandas`, sest selle abil on lihtne sooritada
# aegridade analüüsi.

data = pd.read_csv("data.csv", index_col=0, parse_dates=True)
stocks = data[["GOOG", "T", "AAPL", "GS", "IBM"]].pct_change().fillna(0.0)
data

# Kuvame aktsiahinnad graafikul.

data.plot()
plt.show()

# Sobiva portfoolio väljaselgitamiseks kasutame **Markowitzi meetodit**.
#
# Klassikalises Markowitzi portfoolio optimiseerimise ülesandes vaadeldakse
# $n$ erinevasse aktsiasse (või muusse vääringusse) investeerimist ja
# eeldatakse, et neid säilitatakse mingi ajaperioodi vältel. Tähistagu
# $\omega_j$ väärtpaberisse $j$ investeeritud summat, ja eeldame
# stohhastilist mudelist, mille järgi see väärtpaber annab tagasi
# juhusliku suuruse $r$ teadaoleva keskväärtuse $\mu$ ja kovariatsiooniga $C$.
#
# Arvutame aktsiahindade keskväärtused $\mu$ ja salvestame nad muutujasse `mu`.

mu = stocks.mean()
print mu

# Arvutame kovariatsioonimaatriksi $C$ ning salvestame selle muutujasse `covar`

covar = stocks.cov()
print covar


# Investori ülesandeks on nüüd tagada portfoolio tasakaal. Teisi sõnu tuleb
# leida kompromiss minimaalse riski ja hea tootlikuse vahel, see tähendab
# tuleb leida portfelli *efektiifsusraja*. Toome sisse finantsvõimenduse $L$
# piirangu portfooliole. Võttes $L = 1$ saame klassikalise *long-only*
# portfoolio, samas kui $L = 1.6$ korral saame $130/30$ portfoolio.
#
# Kokkuvõttes saame järgmise optimiseerimisülesande:
#
# $$ \mu^T \omega - \alpha\ \omega^T C \omega \rightarrow \mbox{max} $$
# tingimusel
# $$ \begin{cases}
#     \sum \omega_i = 1, \\
#     \sum | \omega_i | \leq L.
# \end{cases} $$
#
# Defineerime funktsiooni, millega saame *Markowitzi* mudeli järgi
# parameetrile $\alpha$ vastavad kaalud:

# In[6]:

def Markowitz(mu, covar, alpha, L=1.0):
    # defineerime kasutatava mudeli kasutades keskväärtusi
    model = mosek_model.build_model('meanVariance')

    # toome sisse n mitte-negatiivset kaalu
    weights = mosek_model.weights(model, "weights", n=covar.shape[1])

    # leiame kaaludele vastavad finantsvõimendused
    lev = mosek_math.l1_norm(model, "leverage", weights)

    # nõuame, et oleks täidetud tingimus omega_1 + ... + omega_n = 1
    mosek_bound.equal(model, Expr.sum(weights), 1.0)

    # nõuame, et oleks täidetud tingimus |omega_1| + ... + |omega_n| <= L
    mosek_bound.upper(model, lev, L)

    v = Expr.dot(mu.values, weights)

    # arvutame variatsiooni
    var = mosek_math.variance(model, "variance", weights, alpha*covar.values)

    # maksimeerime sihifunktsiooni
    mosek_model.maximise(model, Expr.sub(v, var))

    # arvutame lõpuks kaalud ja tagastame need
    weights = pd.Series(data=np.array(weights.level()), index=stocks.keys())
    return weights


# Lõpuks leiame fikseeritud vektori $\alpha$ ja erinevate finantsvõimenduse
# $L$ korral meie portfellile vastavad efektiivsusrajad ja kanname
# need graafikule.

alphas = [0.1, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

weights_1 = pd.DataFrame({alpha: Markowitz(mu, covar, alpha, L=1.0) for alpha in alphas})
profit_1 = pd.DataFrame({alpha: (stocks * weights_1[alpha]).sum(axis=1) for alpha in weights_1.columns})

weights_16 = pd.DataFrame({alpha: Markowitz(mu, covar, alpha, L=1.6) for alpha in alphas})
profit_16 = pd.DataFrame({alpha: (stocks * weights_16[alpha]).sum(axis=1) for alpha in weights_16.columns})

weights_2 = pd.DataFrame({alpha: Markowitz(mu, covar, alpha, L=2.0) for alpha in alphas})
profit_2 = pd.DataFrame({alpha: (stocks * weights_2[alpha]).sum(axis=1) for alpha in weights_2.columns})

weights_3 = pd.DataFrame({alpha: Markowitz(mu, covar, alpha, L=3.0) for alpha in alphas})
profit_3 = pd.DataFrame({alpha: (stocks * weights_3[alpha]).sum(axis=1) for alpha in weights_3.columns})

plt.figure(figsize=(20, 10))
plt.rcParams['font.size'] = 14

plt.plot(profit_1.std(), profit_1.mean(), label="$L = 1$")
plt.plot(profit_16.std(), profit_16.mean(), label="$L = 1.6$")
plt.plot(profit_2.std(), profit_2.mean(), label="$L = 2$")
plt.plot(profit_3.std(), profit_3.mean(), label="$L = 3$")

plt.legend(loc='best')
plt.title("Efektiivsusrajad")
plt.show()
