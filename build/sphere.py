import cv2
import numpy as np
import matplotlib.pyplot as plt

def one_sphere(img_f):
    #Константы:
    PIXEL_PER_METRIC=1
    WIDTH = 550 # желаемая ширина картинки
    #CENTER_ACCURACY = 10 # допустимая разница между центрами внутренней и внешней сферы
    OFFSET_OUTER=5

    #Переменные
    sphere_outer_radius=200
    center_outer_x = None
    center_outer_y = None
    steps=0

    #Кнопки
    if __name__ == '__main__':
        def nothing(x): 
            pass

    cv2.namedWindow( "settings",cv2.WINDOW_AUTOSIZE )
    cv2.resizeWindow("settings", 350 , 500)  

    #Настройка детектора краёв
    cv2.createTrackbar('Canny_min', 'settings', 200, 250, nothing)
    cv2.createTrackbar('Canny_max', 'settings', 240, 350, nothing)

    # Настройки разброса центра
    cv2.createTrackbar('Center_accuracy', 'settings', 10, 20, nothing)

    #Размытие
    cv2.createTrackbar('Bloor', 'settings', 3, 10, nothing)

    #Кнопки для параметров ПОКА НЕ ПОНЯЛ КАКИХ
    cv2.createTrackbar('param1_outer', 'settings', 150, 300, nothing)
    cv2.createTrackbar('param2_outer', 'settings', 20, 100, nothing)
    cv2.createTrackbar('param1_inner', 'settings', 150, 300, nothing)
    cv2.createTrackbar('param1_inner', 'settings',10, 100, nothing)

    #Кнопки для min и max радиусов при настройке
    cv2.createTrackbar('minRadius_outer', 'settings', 50, 100, nothing)
    cv2.createTrackbar('maxRadius_outer', 'settings', 200, 210, nothing)
    cv2.createTrackbar('minRadius_inner', 'settings', 10, 100, nothing)
    ###

    while True:
        steps+=1
        #Ввод и обрезка инзображения
        img  = cv2.imread(img_f) #'ds_img_benzene/benzene1.jpg' # test_pic/img1.jpg
        img_baz= img
        #img = img[100:920, 100:920]

        #Пропорциональное уменьшение картинки
        new_width=WIDTH
        aspect_ratio= new_width / img.shape[1]
        new_height= int(img.shape[0] * aspect_ratio)
        dim= [new_width,new_height]
        img = cv2.resize(img , dsize=dim , interpolation=cv2.INTER_AREA)

        imgt=img

        ###
        canny_min = cv2.getTrackbarPos('Canny_min', 'settings')
        canny_max = cv2.getTrackbarPos('Canny_max', 'settings')
        bloor = cv2.getTrackbarPos('Bloor', 'settings')

        CENTER_ACCURACY=cv2.getTrackbarPos('Center_accuracy', 'settings')

        param1_outer = cv2.getTrackbarPos('param1_outer', 'settings')
        param2_outer = cv2.getTrackbarPos('param2_outer', 'settings')
        param1_inner = cv2.getTrackbarPos('param1_inner', 'settings')
        param2_inner = cv2.getTrackbarPos('param1_inner', 'settings')
        
        minRadius_outer = cv2.getTrackbarPos('minRadius_outer', 'settings')
        maxRadius_outer = cv2.getTrackbarPos('maxRadius_outer', 'settings')
        minRadius_inner = cv2.getTrackbarPos('minRadius_inner', 'settings')
        ###

        #Меяем цвет на серый и проводим размытие картинки
        if bloor % 2 == 0:
            bloor = bloor + 1

        gray = cv2.cvtColor(imgt, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (bloor, bloor), 0)
        #ret,gray = cv2.threshold(gray,80,255,cv2.THRESH_BINARY)
        ret,gray = cv2.threshold(gray,250,255,cv2.THRESH_TRUNC)
        #ret,gray = cv2.threshold(gray,100,255,cv2.THRESH_TOZERO)
        #ret,gray = cv2.threshold(gray,180,255,cv2.THRESH_TOZERO_INV)

        #Обнаружние ребер и их расширние + слаживает. Т.о убираем разрывы в конурах 
        kernel = np.ones((3,3),np.uint8) # ядро
        edged = cv2.Canny(gray, canny_min, canny_max ) #Нахождение ребер   #200 240
        edged = cv2.dilate(edged, kernel, iterations=1) #утолщение 
        edged = cv2.erode(edged, kernel, iterations=1) # утоньшение

        rows = edged.shape[0]
        #Получение радиуса внешней сферы
        circles = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1, rows,
                                param1 = param1_outer, param2 = param2_outer,
                                minRadius=minRadius_outer, maxRadius=maxRadius_outer)
        #print(circles)
        if circles is None:
            circles= None
        else:     
            circles= np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.circle(imgt,(i[0],i[1]),i[2],(0,255,0),2)#Сама окружность
                cv2.circle(imgt,(i[0],i[1]),2,(0,0,255),3) #центр окружности
            
                sphere_outer_radius=i[2]
                center_outer_x=i[0] 
                center_outer_y=i[1] 

        #Получения радиуса внутренней сферы
        
        circles2 = cv2.HoughCircles(edged, cv2.HOUGH_GRADIENT, 1, rows,
                                    param1=param1_inner, param2=param2_inner,
                                    minRadius=minRadius_inner, maxRadius=sphere_outer_radius-OFFSET_OUTER) 
        if circles2 is None:
            circles2= None
            spher_inner_radius=0
        else:
            circles2= np.uint16(np.around(circles2))
            spher_inner_radius=0
            if center_outer_x is None:
                    for i in circles2[0,:]:
                        cv2.circle(imgt,(i[0],i[1]),i[2],(0,255,0),2) 
                        cv2.circle(imgt,(i[0],i[1]),2,(0,0,255),3)
                        spher_inner_radius=i[2]
                        center_inner_x=i[0] 
                        center_inner_y=i[1]
                        
            else:         
                for i in circles2[0,:]:
                    if i[0]>=(center_outer_x-CENTER_ACCURACY) and i[0]<=(center_outer_x+CENTER_ACCURACY):
                        if i[1]>=(center_outer_y-CENTER_ACCURACY) and i[1]<=(center_outer_y+CENTER_ACCURACY):
                            cv2.circle(imgt,(i[0],i[1]),i[2],(0,255,0),2) 
                            cv2.circle(imgt,(i[0],i[1]),2,(0,0,255),3)
                            spher_inner_radius=i[2]
                            center_inner_x=i[0] 
                            center_inner_y=i[1]

                        #if spher_inner_radius==0:
                        #    print('В радиусе', CENTER_ACCURACY , 'от центра внешней сферы, нет доступных сфер')
            #break
        delta=sphere_outer_radius-spher_inner_radius # разница диаметров 

        #Вывод изображений 
        cv2.imshow('contour', edged)
        cv2.imshow('pic', imgt)                

        if steps==25: # просто для удобства что бы вывод не спамил
            if circles is None and circles2 is None:
                print('Нет доступных сфер')
            else:    
                if circles is None:
                    print(' Внешняя окружность не найдена!' '\n','Внутренний радиус:', spher_inner_radius )
                elif circles2 is None:
                    print(' Внешний радиус: ',sphere_outer_radius)
                else:    
                    print(' Внешний радиус: ',sphere_outer_radius,'\n','Внутренний радиус:', spher_inner_radius , '\n','Разница радиусов:' , delta)          
            steps=0
        #print(sphere_outer_radius, spher_inner_radius , delta)
        ch = cv2.waitKey(100)
        if ch == 27:
            break

    cv2.destroyAllWindows()


#one_sphere('ds_img_benzene_v2/benzene (11).jpg')    
 