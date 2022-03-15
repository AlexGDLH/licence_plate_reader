import cv2
import pytesseract
import openpyxl
import pandas as pd
import csv

pytesseract.pytesseract.tesseract_cmd =

###allows to use the camara
captura = cv2.VideoCapture (0)
while (captura.isOpened()):
    ret, imagen = captura.read ()

   ##change the color to gray
    if ret == True:
        gray = cv2.cvtColor (imagen, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur (gray, (3, 3))
        canny = cv2.Canny (gray, 150, 200)
        canny = cv2.dilate (canny, None, iterations=1)

        cnts, _ = cv2.findContours (canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
####find contours and areas
        for c in cnts:
            area = cv2.contourArea (c)
            x, y, w, h = cv2.boundingRect (c)
            epsilon = 0.09 * cv2.arcLength (c, True)
            approx = cv2.approxPolyDP (c, epsilon, True)

            if len (approx) == 4 and area > 9000:
                cv2.imshow ('video', imagen)
                aspect_ratio = float (w) / h
                if aspect_ratio > 2:
                    placa = gray[y:y + h, x:x + w]
                    text = pytesseract.image_to_string (placa, config='--psm 7')
                    print ('PLACA: ', text)
                    cv2.imshow ('PLACA', placa)
###create an excel file
                    df_marks = pd.DataFrame({'Placas leidas': [ text]})
                    writer = pd.ExcelWriter ('placas.xlsx')

                    with open ("placas.xlsx", "a", newline='') as csvfile:
                        writer = csv.writer (csvfile, delimiter=' ')
                        writer.writerow (["index", "a_name", "b_name"])

                    print ('DataFrame is written successfully to Excel File.')


        cv2.imshow ('video', imagen)
        if cv2.waitKey (1) & 0xFF == ord ('s'):
            break
    else:
        break
captura.release ()
cv2.destroyAllWindows ()
