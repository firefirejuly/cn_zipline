import matplotlib.pyplot as plt
import pandas as pd
perf = pd.read_pickle('cn_zipline/examples/out.pickle') # read in perf DataFrame
perf.head()

ax1 = plt.subplot(211)
perf.portfolio_value.plot(ax=ax1)
ax1.set_ylabel('portfolio value')
ax2 = plt.subplot(212, sharex=ax1)
perf.AAPL.plot(ax=ax2)
ax2.set_ylabel('AAPL stock price')
plt.show()