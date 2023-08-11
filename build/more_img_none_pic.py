import cv2
import os
from sphere_func_v2 import *
import natsort
import csv
import xlsxwriter
import pandas as pd 

def set_param_sphere(directory):

    WIDTH = 550 # желаемая ширина картинки
    sum_img=0
    stat=[['index','outer','inner','inner/outer']]
    sort= natsort.natsorted(os.listdir(directory))
    name_out="tab_"+directory+".csv" # имя нового csv файла

    for filename in sort:
        f = os.path.join(directory, filename)
        sum_img+=1
        print(filename)
        if os.path.isfile(f) and sum_img > 8 and sum_img < 15:
            print(f)
            o,i,cir1,cir2,imgt ,  =func(f)
            stat.append([sum_img,o,i,((o-i)/2)])

    with open(name_out, mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file)
        for line in stat:
            file_writer.writerow(line)            
    stat = pd.DataFrame(stat)        
    writer_obj = pd.ExcelWriter("xlsx_tab_"+directory+'.xlsx',engine='xlsxwriter')
    stat.to_excel(writer_obj, sheet_name='1')
    writer_obj.save()
    return name_out