"""
1.58 mill ticks

ranges of strats - regression at n length then by if alpha etc 

"""

from pylab import figure, show 
from scipy.stats import linregress
import numpy as np
import datetime

def gettime(x):
    dte, tme = x.split(' ')
    dte =list(map(int, dte.split('-')))
    tme = tme.split(':')
    ms = list(map(int, tme[2].split('.')))
    tme = list(map(int, tme[:-1]))
    x = datetime.datetime(dte[0], dte[1], dte[2], tme[0], tme[1], ms[0], ms[1])
    return x

class TickData:
    def __init__(self, filepath):
        buys = []
        sells = []
        with open(filepath, "r") as inp:
    
            for line in inp:
                line = line[:-1].split(',')
                
                line = [i[1:-1] for i in line]
                if line[0] == 'buy':
                    buys.append([gettime(line[1]), float(line[-1])])
                if line[0] == 'sell': 
                    sells.append([gettime(line[1]), float(line[-1])])
                    
                l = len(buys)+len(sells)
                if l%50000==0:
                    print(l, line)
                    
                #if l > 50000: 
                #    break
        
        buys = sorted(buys)
        sells = sorted(sells)
        self.buy_dates, self.buys = zip(*buys)            
        self.sell_dates, self.sells = zip(*sells)
        
        spread = []
        csell = 0
        for n, i in enumerate(self.buy_dates):            
            while True: 
                try:
                    assert csell+1 < len(self.sell_dates)
                except Exception as E:
                    print(repr(E))
                    break
                    
                if self.sell_dates[csell+1] < i:                        
                    csell += 1
                    spread.append([i, self.sell_dates[csell], 
                                    self.buys[n], self.sells[csell]])
                else:
                    break
	
            spread.append([i, self.sell_dates[csell], 
                            self.buys[n], self.sells[csell]])
            
            if n%50000==0:
                print(n, spread[-1])
          
        self.spread = spread
 
if __name__ == '__main__':
    td = TickData('C:\\Users\\Paul\\Downloads\\Fills_BTC_USDT.csv')
    lp = np.log(td.buys)-np.log(td.buys[0])
    for lag in range(1000, 100000, 1000):
        for lead in range(1000, lag+1, 1000):
            x = [[],[]]
            for i in range(lag, len(lp)-lead):
                x[0].append(lp[i]-lp[i-lag])
                x[1].append(lp[i+lead]-lp[i+1])
				
            T = np.sum(x[1])
            for k in [0, 0.001, 0.01]:
                xup = [x[1][i] for i in range(len(x[1])) if x[0][i] > k]
                xdown = [x[1][i] for i in range(len(x[1])) if x[0][i] < -k]
                print(lag, lead, k, T, np.sum(xup), len(xup), np.sum(xdown), len(xdown))
                with open('results.txt', 'a') as out:
                    out.write(','.join(list(map(str, [lag, lead, k, T, np.sum(xup), len(xup), np.sum(xdown), len(xdown)])))+'\n')
	
	
	