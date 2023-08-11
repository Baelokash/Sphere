#import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

def graph(file , folder_out_way):
    df=pd.read_csv(file)
    plt.subplot(311)
    df['inner'].plot(linestyle='--', marker='.', color='r')
    plt.title('Inner radius')
    plt.subplot(312)
    df['outer'].plot(linestyle='-.', marker='.', color='b')
    plt.title('Outer radius')
    plt.subplot(313)

    plt.title('(Outer-Inner)/2')
    df['(outer-inner)/2'].plot(linestyle='-', marker='.', color='g')
    plt.tight_layout ()
    file_graphic=folder_out_way+'/fig.png'
    plt.savefig(file_graphic , dpi = 150)
    return file_graphic
  
