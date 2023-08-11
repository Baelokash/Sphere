import numpy as np
import matplotlib.pyplot as plt

def data_processing(stat):
        a=[]
        for row in stat:
         a.append(row[3])
        stat = a[1:]                      
        max_stat=[]
        mid_stat=[]   
        for i in range(len(stat)):
            if stat[i]>(max(stat)*0.9):
                max_stat.append(stat[i])
            elif stat[i]>(max(stat)*0.1):
                mid_stat.append(stat[i])
        print(max_stat , ' ', mid_stat)
        max_mid = sum(max_stat)/len(max_stat)
        mid_mid = sum(mid_stat)/len(mid_stat)            
        print(max_mid , ' ' ,mid_mid)


        N= len(mid_stat)
        y = mid_stat
        x= np.array(range(len(mid_stat)))

        mx = sum(x)/N
        my = sum(y)/N
        a2= np.dot(x.T,x)/N
        a11 = np.dot(x.T,y)/N

        k = (a11 - mx*my)/(a2 - mx**2)
        b = my - k*mx
        f= np.array([k*z+b for z in range(N)])

        #plt.plot(f , c='red')
        #plt.scatter(x , y , s=2 , c ='red')
        #plt.grid(True)
        #plt.show()
        
        k = round(k, 2)
        b = round(b , 2)
        return k , b , max_mid
#stat = [['index', 'outer', 'inner', '(outer-inner)/2'], [8, 103, 83, 10.0], [9, 104, 81, 11.5], [10, 107, 78, 14.5], [11, 107, 78, 14.5], [12, 108, 75, 16.5], [13, 109, 73, 18.0], [14, 111, 70, 20.5], [15, 112, 69, 21.5], [16, 114, 67, 23.5], [17, 114, 64, 25.0], [18, 115, 63, 26.0], [19, 117, 62, 27.5], [20, 117, 60, 28.5], [21, 117, 58, 29.5], [22, 119, 57, 31.0]] 
#data_processing(stat)