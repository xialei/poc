__author__ = 'roger'

from numpy import vstack

from scipy.cluster.vq import kmeans, vq
from matplotlib.finance import quotes_historical_yahoo
from datetime import datetime

start = datetime(2015,7,1)
end = datetime(2015,9,30)

listDji = ['AXP','BA','CAT','CSCO','CVX','DD','DIS','GE','GS','HD','IBM', 'INTC','JNJ','JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','T','TRV', 'UNH','UTX','V','VZ','WMT','XOM']

quotes = [[0 for col in range(90)] for row in range(30)]
listTemp = [[0 for col in range(90)] for row in range(30)]
for i in range(30):
    quotes[i] = quotes_historical_yahoo(listDji[i], start, end)

days = len(quotes[0])

for i in range(30):
    for j in range(days-1):
        if(quotes[i][j][2] and quotes[i][j+1][2] and (quotes[i][j+1][2] >= quotes[i][j][2])):
            listTemp[i][j] = 1.0
        else:
            listTemp[i][j] = -1.0

data = vstack(listTemp)
centroids,_ = kmeans(data, 4)
result,_ = vq(data, centroids)
print(result)