from __future__ import division
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import pandas as pd

raw_data=pd.read_csv("../assets/combinedData.csv")
obesityLADs=raw_data[['LAD22NM','Obesity Percentage (18+)']].drop_duplicates()
sortedObesityLADs=obesityLADs.sort_values(by='Obesity Percentage (18+)', ascending=True)
overweightLADs=raw_data[['LAD22NM','Overweight Percentage (18+)']].drop_duplicates()
sortedOverweightLADs=overweightLADs.sort_values(by='Overweight Percentage (18+)', ascending=True)

ax = sortedObesityLADs.plot.barh(y="Obesity Percentage (18+)",x='LAD22NM',rot=0)
#ax = sortedOverweightLADs.plot.barh(x='LAD22NM',y="Overweight Percentage (18+)",rot=0)
ax.set_ylabel("Local Authority District")
ax.set_xlabel("Percentage of adults that are obese")
#ax.set_xlabel("Percentage of adults that are overweight")
ax.get_legend().remove()
plt.tight_layout()
plt.rcParams["figure.figsize"]=(36,15)
plt.savefig("../assets/Obesity_Distribution.png",dpi=100)
#plt.savefig("../assets/Overweight_Distribution.png",dpi=100)

