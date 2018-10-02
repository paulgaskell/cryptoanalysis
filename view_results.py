
from pylab import figure, show
from cryptoanalysis_python3 import TickData
import numpy as np

def get_results():
    with open('results.txt', 'r') as inp:
        lines = inp.readlines()
        
    lines = [list(map(float, i[:-1].split(','))) for i in lines]
    x = [i for i in lines if i[4] > 0 or i[6] > 0]

    mx = 0
    for n, i in enumerate(x):
        if i[4] > mx:
            mx = i[4]
            print(i)

    # x, y axis 
    fig = figure()
    axs = [fig.add_subplot(221), fig.add_subplot(222), fig.add_subplot(223)]
    axs[0].scatter([i[0] for i in x], [i[1] for i in x])
    axs[1].plot(sorted([i[4] for i in x]))
    axs[1].plot(sorted([i[6] for i in x]))
    axs[2].scatter([i[4] for i in x], [i[6] for i in x])
    show()

def get_single_result(lag, lead, s):
    td = TickData('C:\\Users\\Paul\\Downloads\\Fills_BTC_USDT.csv')
    lp = np.log(td.buys)-np.log(td.buys[0])
    x = [[],[],[]]
    for i in range(lag, len(lp)-lead):
        x[0].append(lp[i]-lp[i-lag])
        x[1].append(lp[i+lead]-lp[i+1])
        x[2].append(lp[i+1])
				
    T = np.sum(x[1])
    for k in [0, 0.001, 0.01]:
        xup = [x[1][i] for i in range(len(x[1])) if x[0][i] > k]
        xdown = [x[1][i] for i in range(len(x[1])) if x[0][i] < -k]
        print(lag, lead, k, T, np.sum(xup), len(xup), np.sum(xdown), len(xdown))

    g = []
    h = [[]]
    i = 0
    while i < len(x[0]):
        if x[0][i] > s:
            for j in range(i, i+lead):
                g.append(x[2][j])
                h[-1].append(x[2][j])
            i = j+1
        else:
            i += 1
            g.append(float('inf'))
            h.append([])
            
    T = 0
    for i in h:
        if len(i) > 0:
            print(i[-1]-i[0], sum(np.diff(i)), len(i))

            
    fig = figure()
    ax = fig.add_subplot(211)
    ax1 = fig.add_subplot(212)
    ax.plot(x[2])
    ax.plot(g)
    #ax.plot([x[2][i] if x[0][i] > s else float('inf') for i in range(len(x[2]))])
    show()

if __name__ == '__main__':
    #get_results()
    get_single_result(33000, 25000, 0.01)