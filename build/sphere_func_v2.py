import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

def func(f , settings):
#Константы:

    PIXEL_PER_METRIC=1
    WIDTH = 550 # желаемая ширина картинки
    CENTER_ACCURACY = 5 # допустимая разница между центрами внутренней и внешней сферы
    OFFSET_OUTER=10

#Переменные:
    volume_circle=0  # количество нарисованных окружностей
    sphere_outer_radius=200
    center_outer_x = None
    center_outer_y = None
    center_inner_x = 0
    center_inner_y = 0
    steps=0
    volume_compar = 0 #Счетчик количества пересечений
    slice=0
###
#Стартовые параметры поиска

    canny_min,canny_max = 200,240
    bloor = 3

    param1_outer ,param2_outer  = 150 , 20
    param1_inner,param2_inner = 150, 10
    if settings[0] != None:
         maxRadius_outer = settings[0]
    else:
         maxRadius_outer=150

    if settings[1] != None:
         minRadius_outer = settings[1]
    else:
         minRadius_outer=80  

    if settings[2] != None:
         minRadius_inner = settings[1]
    else:
         minRadius_inner=2      
###

    while True:
        img=cv2.imread(f)
        #Пропорциональное уменьшение картинки
        new_width=WIDTH
        aspect_ratio= new_width / img.shape[1]
        new_height= int(img.shape[0] * aspect_ratio)
        dim= [new_width,new_height]
        img = cv2.resize(img , dsize=dim , interpolation=cv2.INTER_AREA)

        imgt=img
        #Заготовки для определения наличия перечений окружностей:
        compar1 = np.zeros(shape=[550, 550, 1]) # пусто
        compar2 = np.zeros(shape=[550, 550, 1]) # не понимаю для чего нам нужна вторая маска , но это работает


        #Меяем цвет на серый и проводим размытие картинки
        if bloor % 2 == 0:
            bloor = bloor + 1

        gray = cv2.cvtColor(imgt, cv2.COLOR_BGR2GRAY)
        ret,gray = cv2.threshold(gray,110,255,cv2.THRESH_TRUNC)

        #Обнаружние ребер ->их расширние и слаживание, т.о убираем разрывы в конурах 
        kernel = np.ones((3,3),np.uint8) # ядро преобразований
        edged = cv2.Canny(gray, canny_min, canny_max ) 
        edged = cv2.dilate(edged, kernel, iterations=1) #утолщение 
        edged = cv2.erode(edged, kernel, iterations=1) # утоньшение

        rows = edged.shape[0]

        #Получение радиуса внешней сферы
        circles = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1, rows/4,
                                param1 = param1_outer, param2 = param2_outer,
                                minRadius=minRadius_outer, maxRadius=maxRadius_outer)
        if circles is None:
            circles= None
            center_outer_x=0 
            center_outer_y=0
        else:
            if len(circles) > 1:
                circles = circles[0] 
                    
            circles= np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.circle(compar1,(i[0],i[1]),i[2],1,2)
                cv2.circle(imgt,(i[0],i[1]),i[2],(0,255,0),2)#Сама окружность
                cv2.circle(imgt,(i[0],i[1]),2,(0,0,255),3) #центр окружности
            
                sphere_outer_radius=i[2]
                center_outer_x=i[0] 
                center_outer_y=i[1]
                volume_circle+=1 

        #Получения радиуса внутренней сферы
        circles2 = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1, rows/4,
                                    param1=param1_inner, param2=param2_inner,
                                    minRadius=minRadius_inner, maxRadius=sphere_outer_radius-OFFSET_OUTER) 
        
        if circles2 is None:
            spher_inner_radius=0
        else:
            circles2= np.uint16(np.around(circles2))
            spher_inner_radius=0
            if circles is None:
                    for i in circles2[0,:]:
                        cv2.circle(compar2,(i[0],i[1]),i[2],1,2)
                        cv2.circle(imgt,(i[0],i[1]),i[2],(0,255,0),2) 
                        cv2.circle(imgt,(i[0],i[1]),2,(0,0,255),3)
                        spher_inner_radius=i[2]
                        center_inner_x=i[0] 
                        center_inner_y=i[1]
                        volume_circle+=1
            else:         
                for i in circles2[0,:]:
                    if i[0]>=(center_outer_x-CENTER_ACCURACY) and i[0]<=(center_outer_x+CENTER_ACCURACY):
                        if i[1]>=(center_outer_y-CENTER_ACCURACY) and i[1]<=(center_outer_y+CENTER_ACCURACY):
                            cv2.circle(compar2,(i[0],i[1]),i[2],1,2)
                            cv2.circle(imgt,(i[0],i[1]),i[2],(0,255,0),2) 
                            cv2.circle(imgt,(i[0],i[1]),2,(0,0,255),3)
                            spher_inner_radius=i[2]
                            center_inner_x=i[0] 
                            center_inner_y=i[1]
                            volume_circle+=1 

        delta=sphere_outer_radius-spher_inner_radius # разница диаметров
        
        #Определение наличия пересечений
        for i in range(len(compar1)):
            for j in  range(len(compar1[i])):
                if compar1[i][j]==compar2[i][j] and compar2[i][j]==255:
                    volume_compar+=1
        if center_outer_x==None:
             center_outer_x=0
        if  len(edged[center_outer_y])>412:
             length=412
        else:
             length=len(edged[center_outer_y])                    
        for j in  range(length): #150 надо изменить ! проблемма из-за разных длин ширины и высоты
            #print(edged[center_outer_x][j])
            if edged[center_outer_y][j]==255:
                slice+=1
                if slice>4:
                    slice=4                    
        #cv2.imshow('!', edged)           
        #cv2.waitKey(100)
        if  (center_outer_x is None) or (center_outer_y is None):
             center_outer_x=0
             center_outer_y=0
        #print(sphere_outer_radius,spher_inner_radius,' Пересечений:', volume_compar ,'Кличество окружностей:', volume_circle) #center_outer_x , center_inner_x ,volume_compar )
        if sphere_outer_radius>spher_inner_radius and volume_compar==0  and (volume_circle==1 or volume_circle==2) and ((slice/2)==volume_circle): #Имеет ли смысл ставиьт не жёсткое ограничение на volume_compar
                    steps=0
                    volume_compar=0
                    volume_circle=0
                    cir1=[center_outer_x,center_outer_y]
                    cir2=[center_inner_x,center_inner_y]
                    return sphere_outer_radius , spher_inner_radius , cir1 , cir2, imgt 
        else:
            if steps<=10:
                canny_min = random.randint(100, 200)
                canny_max = random.randint(200, 300)
                bloor = random.randint(3, 9)
                #CENTER_ACCURACY =random.randint(4 , 12)
                param1_outer = random.randint(100, 200)
                param2_outer  = random.randint(2, 40)
                param1_inner = random.randint(100, 200)
                param2_inner = random.randint(2, 30)

                steps+=1

            else:
                 steps=0
                 volume_compar=0
                 volume_circle=0
                 cir1=[center_outer_x,center_outer_y]
                 cir2=[center_inner_x,center_inner_y]
                 return sphere_outer_radius , spher_inner_radius , cir1 , cir2 , imgt
        slice=0
        volume_compar=0 
        volume_circle=0    