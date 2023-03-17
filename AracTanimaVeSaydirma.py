import cv2
import numpy as np

#Kamera Kullanılacaksa Kamera Girişi
#kamera = cv2.VideoCapture(0) 

video = cv2.VideoCapture('AracTanimaVeSaydirma.mp4') #Video Girişi

gelis_sol_serit = 0
gelis_sag_serit = 0

gidis_sol_serit = 0
gidis_sag_serit = 0

minimum_genislik = 75
minimum_yükseklik = 75

def AracTespit():
    global gelis_sol_serit
    global gelis_sag_serit

    global gidis_sol_serit
    global gidis_sag_serit

    for contour in contours:
        #Tespit edilen konturun yerlerini hesaplama
        (x, y, w, h) = cv2.boundingRect(contour)
        #Minimum genişlik ve yükseliğe göre kontrol
        contour_kontrol = (w >= minimum_genislik) and (h >= minimum_yükseklik)

        if not contour_kontrol:
            continue
        
        #Tespit edilen konturu dikdörtgen içerisine alma
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (255, 0, 0), 2)
        #Araç üzerine tespit edilde yazdırma
        cv2.putText(frame2, 'Tespit Edildi', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 255), 1, cv2.LINE_AA)
        
        merkez = MerkezAl(x, y, w, h)
        merkezX = merkez[0]
        merkezY = merkez[1]

        cv2.circle(frame1, merkez, 3, (0, 0, 255), -1)
        
        #Şerit sistemine göre geçti geçmedi tespiti
        if(320<merkezX<=475 and 300<merkezY<330):      
            gelis_sol_serit = gelis_sol_serit + 1
            cv2.line(frame2, (320,310), (455,310), (0,0,255), 2)

        elif(475<merkezX<=600 and 300<merkezY<336):
            gelis_sag_serit = gelis_sag_serit + 1
            cv2.line(frame2, (475,310), (600,310), (0,0,255), 2)
            
        elif(700<merkezX<=900 and 550<merkezY<580):
            gidis_sol_serit = gidis_sol_serit + 1
            cv2.line(frame2, (710,570), (880,570), (0,255,0), 2)           

        elif(900<merkezX<=1100 and 530<merkezY<580):
            gidis_sag_serit = gidis_sag_serit + 1
            cv2.line(frame2, (900,570), (1100,570), (0,255,0), 2)
            
def MerkezAl(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)        

while True:
    _, frame1 = video.read()
    _, frame2 = video.read()

    difference = cv2.absdiff(frame1, frame2) #Hareketi tespit etmek için arka plan kaldırma
    gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY) #Görüntüyü gri seviyeli görüntüye çevirme
    blur = cv2.GaussianBlur(gray, (9,9), 0) #Görüntüyü yumuşatma işlemi
    ret, thresh = cv2.threshold(blur, 10, 255, cv2.THRESH_BINARY) #Görüntüde ki hareketli kısımların beyazlaştırılması
    dilate = cv2.dilate(thresh, np.ones((3, 3))) #Dilate metodu ile beyaz alanların büyütülmesi
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2)) #Matrisleri elips şeklinde almak
    closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel) #Siyah alanları küçültmek için closing metodu
    contours, hierarchy = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Araçları tespit etmek için findContours metodu

    frame2 = frame1

    cv2.line(frame2,(320,310),(455,310),(255,255,255),2)
    cv2.putText(frame2, "{}".format(gelis_sol_serit), (445, 300),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.line(frame2,(475,310),(600,310),(255,255,255),2)
    cv2.putText(frame2, "{}".format(gelis_sag_serit), (590, 300),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.line(frame2,(710,570),(880,570),(255,255,255),2)
    cv2.putText(frame2, "{}".format(gidis_sol_serit), (710, 560),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.line(frame2,(900,570),(1100,570),(255,255,255),2)
    cv2.putText(frame2, "{}".format(gidis_sag_serit), (900, 560),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.putText(frame2, "Toplam Arac Sayisi: {}".format(gelis_sol_serit + gelis_sag_serit + gidis_sol_serit + gidis_sag_serit), (10, 250),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(frame2, "Gelen Arac Sayisi: {}".format(gelis_sol_serit + gelis_sag_serit), (10, 275),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(frame2, "Giden Arac Sayisi: {}".format(gidis_sol_serit + gidis_sag_serit), (10, 300),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)    

    AracTespit()
   
    cv2.imshow("Arac Takip ve Saydirma", frame2)
    #cv2.imshow("Frame2", frame2)
    #cv2.imshow("Difference", difference)
    #cv2.imshow("Blur", blur)
    #cv2.imshow("Thresh", thresh)
   
    key = cv2.waitKey(30)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()