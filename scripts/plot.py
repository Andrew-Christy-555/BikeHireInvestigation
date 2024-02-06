from __future__ import division
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import pandas as pd

raw_data=pd.read_csv("combinedData.csv")
obesityLADs=raw_data[['LAD22NM','Obesity Percentage (18+)']].drop_duplicates()
sortedObesityLADs=obesityLADs.sort_values(by='Obesity Percentage (18+)', ascending=True)
overweightLADs=raw_data[['LAD22NM','Overweight Percentage (18+)']].drop_duplicates()
sortedOverweightLADs=overweightLADs.sort_values(by='Overweight Percentage (18+)', ascending=True)

#ax = sortedObesityLADs.plot.barh(x='LAD22NM',y="Obesity Percentage (18+)",rot=0)
ax = sortedOverweightLADs.plot.barh(x='LAD22NM',y="Overweight Percentage (18+)",rot=0)
ax.set_xlabel("Local Authority District")
#ax.set_ylabel("Percentage of adults that are obese")
ax.set_ylabel("Percentage of adults that are overweight")
plt.tight_layout()
#plt.savefig("Obesity_Distribution.png")
plt.savefig("Overweight_Distribution.png")

