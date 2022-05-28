import cv2
import inline as inline
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QLabel, QRadioButton, QPushButton, QVBoxLayout, QApplication, QWidget, QFileDialog)

x = 0

def initializare():
    guiul.lblTxtPoza1.setText("Poza Originala:")
    resetare()
    global path_a
    path_a = r'D:\\Faculta\\Recunoasterea Formelor\\Lab\\m4\\pozeModificate\\1.jpg';
    global path_alfa
    path_alfa = r"D:\\Faculta\\Recunoasterea Formelor\\Lab\\m4\\pozeModificate\\PozaCautata.jpg";
    guiul.btnStanga.setVisible(False)
    guiul.btnDreapta.setVisible(False)
    guiul.btnInc.setVisible(False)
    guiul.slider.setVisible(False)
    guiul.lblProcent.setVisible(False)
    guiul.txtX.setVisible(False)
    guiul.txtY.setVisible(False)
    guiul.txtZ.setVisible(False)
    guiul.txtW.setVisible(False)
    guiul.btnDate.setVisible(False)
    guiul.lblDimensiune.setVisible(False)

def reshape(imagine):
    scale_percent = 60
    width = int(imagine.shape[1] * scale_percent / 100)
    height = int(imagine.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(imagine, dim, interpolation=cv2.INTER_AREA)
    return resized
def reshape_sever(imagine):
    scale_percent = 40
    width = int(imagine.shape[1] * scale_percent / 100)
    height = int(imagine.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(imagine, dim, interpolation=cv2.INTER_AREA)
    return resized

def cautaPrimaPoza():
    filename = QFileDialog.getOpenFileName()
    global path
    path = filename[0]
    imagine = cv2.imread(path)
    imagine = reshape(imagine)
    cv2.imwrite(path_alfa, imagine)
    global pixmap
    pixmap = QPixmap(path_alfa)
    guiul.lblPoza1.setPixmap(pixmap)

def lineDet():
    imagine = cv2.imread(path)
    imagine = reshape(imagine)
    imagine = cv2.cvtColor(imagine, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(imagine, cv2.COLOR_BGR2GRAY)
    # Canny Edges
    edges = cv2.Canny(gray, 100, 170, apertureSize=3)

    # Run HoughLines Fucntion
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
    # Run for loop through each line
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x_1 = int(x0 + 1000 * (-b))
        y_1 = int(y0 + 1000 * (a))
        x_2 = int(x0 - 1000 * (-b))
        y_2 = int(y0 - 1000 * (a))
        cv2.line(imagine, (x_1, y_1), (x_2, y_2), (255, 0, 0), 2)

    cv2.imwrite(path_a, edges)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("Edges")

    cv2.imwrite(path_a, imagine)
    pixmap = QPixmap(path_a)
    guiul.lblPoza3.setPixmap(pixmap)
    guiul.lblTxtPoza3.setText("Transformata Hough")


def prima():
    imagine = cv2.imread(path)
    print(path)
    imagine_gri = cv2.cvtColor(imagine, cv2.COLOR_BGR2GRAY)
    imagine_gri = reshape(imagine_gri)
    cv2.imwrite(path_a, imagine_gri)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("Poza in Gri")

    imagine_hsv = cv2.cvtColor(imagine, cv2.COLOR_BGR2HSV)
    imagine_hsv = reshape(imagine_hsv)
    cv2.imwrite(path_a, imagine_hsv)
    pixmap2 = QPixmap(path_a)
    guiul.lblPoza3.setPixmap(pixmap2)
    guiul.lblTxtPoza3.setText("Poza in HSV")

def resize():
    imagine = cv2.imread(path)

    imagine_lineara = cv2.resize(imagine, (280, 280), interpolation=cv2.INTER_LINEAR)
    cv2.imwrite(path_a, imagine_lineara)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("Linear")

    imagine_nearest = cv2.resize(imagine, (280, 280), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(path_a, imagine_nearest)
    pixmap = QPixmap(path_a)
    guiul.lblPoza3.setPixmap(pixmap)
    guiul.lblTxtPoza3.setText("Nearest")

    imagine_cubic = cv2.resize(imagine, (280, 280), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(path_a, imagine_cubic)
    pixmap = QPixmap(path_a)
    guiul.lblPoza4.setPixmap(pixmap)
    guiul.lblTxtPoza4.setText("Cubic")

    imagine_lanczos = cv2.resize(imagine, (280, 280), interpolation=cv2.INTER_LANCZOS4)
    cv2.imwrite(path_a, imagine_lanczos)
    pixmap = QPixmap(path_a)
    guiul.lblPoza5.setPixmap(pixmap)
    guiul.lblTxtPoza5.setText("Lanczos")

    imagine_area = cv2.resize(imagine, (280, 280), interpolation=cv2.INTER_AREA)
    cv2.imwrite(path_a, imagine_area)
    pixmap = QPixmap(path_a)
    guiul.lblPoza6.setPixmap(pixmap)
    guiul.lblTxtPoza6.setText("Area")

def rotatie_stanga():
    global x
    x += 45
    rotatie()

def rotatie_dreapta():
    global x
    x -= 45
    rotatie()

def rotatie():
    guiul.btnStanga.setVisible(True)
    guiul.btnDreapta.setVisible(True)
    imagine = cv2.imread(path)
    imagine = reshape(imagine)
    rows, cols = imagine.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), x, 1)
    dst = cv2.warpAffine(imagine, M, (cols, rows))
    cv2.imwrite(path_a, dst)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("Oglindire")

def crop():
    imagine = cv2.imread(path)
    x = guiul.txtX.toPlainText()
    y = guiul.txtY.toPlainText()
    z = guiul.txtZ.toPlainText()
    w = guiul.txtW.toPlainText()
    imagine = reshape(imagine)
    cropped_image = imagine[int(x):int(y),int(z):int(w)]
    cv2.imwrite(path_a, cropped_image)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("Cropped")

def crop_initiere():
    guiul.txtX.setVisible(True)
    guiul.txtY.setVisible(True)
    guiul.txtZ.setVisible(True)
    guiul.txtW.setVisible(True)
    guiul.btnDate.setVisible(True)
    guiul.lblDimensiune.setVisible(True)
    imagine = cv2.imread(path)
    imagine = reshape(imagine)
    h, w, _ = imagine.shape
    guiul.lblDimensiune.setText("Poza are inaltimea de "+str(h)+" pixeli si latimea de "+str(w)+" pixeli :)")

def thresholding():
    imagine = cv2.imread(path)
    imagine_gri = cv2.cvtColor(imagine, cv2.COLOR_BGR2GRAY)
    imagine_gri = reshape(imagine_gri)

    ret, thresh_binary = cv2.threshold(imagine_gri, 127, 255, cv2.THRESH_BINARY)
    ret, thresh_binary_inv = cv2.threshold(imagine_gri, 127, 255, cv2.THRESH_BINARY_INV)
    ret, thresh_trunc = cv2.threshold(imagine_gri, 127, 255, cv2.THRESH_TRUNC)
    ret, thresh_tozero = cv2.threshold(imagine_gri, 127, 255, cv2.THRESH_TOZERO)
    ret, thresh_tozero_inv = cv2.threshold(imagine_gri, 127, 255, cv2.THRESH_TOZERO_INV)

    cv2.imwrite(path_a, thresh_binary)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("thresh_binary")

    cv2.imwrite(path_a, thresh_binary_inv)
    pixmap = QPixmap(path_a)
    guiul.lblPoza3.setPixmap(pixmap)
    guiul.lblTxtPoza3.setText("thresh_binary_inv")

    cv2.imwrite(path_a, thresh_trunc)
    pixmap = QPixmap(path_a)
    guiul.lblPoza4.setPixmap(pixmap)
    guiul.lblTxtPoza4.setText("thresh_trunc")

    cv2.imwrite(path_a, thresh_tozero)
    pixmap = QPixmap(path_a)
    guiul.lblPoza5.setPixmap(pixmap)
    guiul.lblTxtPoza5.setText("thresh_tozero")

    cv2.imwrite(path_a, thresh_tozero_inv)
    pixmap = QPixmap(path_a)
    guiul.lblPoza6.setPixmap(pixmap)
    guiul.lblTxtPoza6.setText("thresh_tozero_inv")

def edgeDetection():
    imagine = cv2.imread(path)
    imagine = reshape(imagine)
    edges = cv2.Canny(imagine, 200, 200)

    cv2.imwrite(path_a, edges)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("")

def fa_ceva():
    nr = guiul.lblProcent.text()
    bluru(nr)

def bluru(r):
    nr = int(r)
    print(nr)
    imagine = cv2.imread(path)
    imagine = reshape(imagine)
    ksize = (nr, nr)
    imagine = cv2.blur(imagine, ksize)
    cv2.imwrite(path_a, imagine)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("")

def blur():
    guiul.btnInc.setVisible(True)
    guiul.slider.setVisible(True)
    guiul.lblProcent.setVisible(True)

    imagine = cv2.imread(path)
    imagine = reshape(imagine)

    ksize = (10, 10)
    imagine = cv2.blur(imagine, ksize)
    cv2.imwrite(path_a, imagine)
    pixmap = QPixmap(path_a)
    guiul.lblPoza2.setPixmap(pixmap)
    guiul.lblTxtPoza2.setText("")

def verificareAlegeri():
    if guiul.rdbGrey.isChecked():
        prima()
    if guiul.rdbResize.isChecked():
        resize()
    if guiul.rdbOglinda.isChecked():
        rotatie()
    if guiul.rdbTresh.isChecked():
        thresholding()
    if guiul.rdbEdge.isChecked():
        edgeDetection()
    if guiul.rdbCrop.isChecked():
        crop_initiere()
    if guiul.rdbBlur.isChecked():
        blur()
    if guiul.rdbLines.isChecked():
        lineDet()

def resetare():
    guiul.lblPoza2.clear()
    guiul.lblPoza3.clear()
    guiul.lblPoza4.clear()
    guiul.lblPoza5.clear()
    guiul.lblPoza6.clear()
    guiul.lblTxtPoza2.clear()
    guiul.lblTxtPoza3.clear()
    guiul.lblTxtPoza4.clear()
    guiul.lblTxtPoza5.clear()
    guiul.lblTxtPoza6.clear()
    guiul.btnStanga.setVisible(False)
    guiul.btnDreapta.setVisible(False)
    guiul.btnInc.setVisible(False)
    guiul.slider.setVisible(False)
    guiul.lblProcent.setVisible(False)
    guiul.txtX.setVisible(False)
    guiul.txtY.setVisible(False)
    guiul.txtZ.setVisible(False)
    guiul.txtW.setVisible(False)
    guiul.btnDate.setVisible(False)
    guiul.lblDimensiune.setVisible(False)


app = QtWidgets.QApplication([])
guiul = uic.loadUi("gui.ui")

guiul.btnCautaPoza.clicked.connect(cautaPrimaPoza)
guiul.btnResetare.clicked.connect(resetare)
guiul.btnValideaza.clicked.connect(verificareAlegeri)
guiul.btnStanga.clicked.connect(rotatie_stanga)
guiul.btnDreapta.clicked.connect(rotatie_dreapta)
guiul.btnInc.clicked.connect(fa_ceva)
guiul.btnDate.clicked.connect(crop)
initializare()

guiul.show()
app.exec()
