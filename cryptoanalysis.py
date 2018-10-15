"""

"""

from pylab import figure, show 
from scipy.stats import linregress
import numpy as np
import datetime
import json

def gettime(x):
    dte, tme = x.split(' ')
    dte = map(int, dte.split('-'))
    tme = tme.split(':')
    ms = map(int, tme[2].split('.'))
    tme = map(int, tme[:-1])
    x = datetime.datetime(dte[0], dte[1], dte[2], tme[0], tme[1], ms[0], ms[1])
    return x

def roundtime(x):
    dte, tme = x.split(' ')
    dte = map(int, dte.split('-'))
    tme = tme.split(':')
    ms = map(int, tme[2].split('.'))
    tme = map(int, tme[:-1])
    x = datetime.datetime(dte[0], dte[1], dte[2], tme[0], tme[1], 0, 0)
    return x    
    
class TickData:
    def __init__(self, filepath):
		
		self.filepath = filepath
		
    def load_all_data(self):
	
        buys = []
        sells = []
        with open(filepath, "r") as inp:

            for line in inp:
                line = line[:-1].split(',')
                #print(line)
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

    def load_buys(self, brk=1000000000):
        buys = []
        with open(self.filepath, "r") as inp:

            for line in inp:
                line = line[:-1].split(',')
                #print(line)
                line = [i[1:-1] for i in line]
                if line[0] == 'buy':
                    buys.append([gettime(line[1]), float(line[-1])])
                if line[0] == 'sell': 
                    break
                    
                l = len(buys)
                if l%50000==0:
                    print(l, line)	
                if l > brk:
                    break

        buys = sorted(buys)
        self.buy_dates, self.buys = zip(*buys)                     
    
    def load_seconds(self, brk=100000000):
        buys = {}
        with open(self.filepath, "r") as inp:

            for line in inp:
                line = line[:-1].split(',')
                #print(line)
                line = [i[1:-1] for i in line]
                rtme = round
                if line[0] == 'buy':

                    buys.append([gettime(line[1]), float(line[-1])])
                if line[0] == 'sell': 
                    break
                    
                l = len(buys)
                if l%50000==0:
                    print(l, line)	
                if l > brk:
                    break

        buys = sorted(buys)
        self.buy_dates, self.buys = zip(*buys)         
     
if __name__ == '__main__':
    td = TickData('C:\\Users\\Paul\\Downloads\\Fills_BTC_USDT.csv')
    td.load_buys()
    lp = np.log(td.buys)-np.log(td.buys[0])
    r = np.diff(lp)
    mdls = []
    for lag in range(50, 91, 10):
        for lead in range(10, lag+1, 10):
            mdls.append((lag, lead))

    for lag, lead in mdls[:]:
        x = np.zeros(len(lp))
        signals = np.zeros(len(lp))
        signals_p = np.zeros(len(lp))
        for i in range(lag, len(lp)-lead):
            x[i] = (lp[i]-lp[i-lag])
            signals_p[i+1:i+lead] += x[i]
            if x[i] > 0:
                signals[i+1:i+lead] += 1
            else:
                signals[i+1:i+lead] -= 1
                
            if i%50000 == 0:
                print i
        
        sgn_s = np.sign(np.array(signals[1:]))
        sgn_sp = np.sign(np.array(signals_p[1:]))
        s = sum(np.diff(lp)*sgn_s)
        sp = sum(np.diff(lp)*sgn_sp)
        trds_s = len([i for i in range(1, len(sgn_s)) if sgn_s[i] != sgn_s[i-1]])
        trds_sp = len([i for i in range(1, len(sgn_sp)) if sgn_sp[i] != sgn_sp[i-1]])
                        
        print lag, lead, s, sp, trds_s, trds_sp
        jsn = { 'lag': lag, 'lead': lead, 's': s, 'sp': sp, 
                'trds_s': trds_s, 'trds_sp': trds_sp }
        with open('signals.njson', 'a') as out:
            out.write(json.dumps(jsn)+'\n')

		
