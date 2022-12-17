import sys
import os
import time

import pyaudio
import wave
import librosa
import numpy as np

import pandas as pd
import random
import pygame.mixer

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QFontDatabase

from tensorflow.python.keras.models import load_model



def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#############   MAIN 윈도우   #################
form_main = resource_path(".//ui//main.ui")
form_main_class = uic.loadUiType(form_main)[0]
##############################################

#########   trainselect 윈도우   ##############
form_trainselect = resource_path(".//ui//trainselect.ui")
form_trainselect_class = uic.loadUiType(form_trainselect)[0]
##############################################

#########   nowtrain 윈도우   ##############
form_nowtrain = resource_path(".//ui//nowtrain.ui")
form_nowtrain_class = uic.loadUiType(form_nowtrain)[0]
##############################################

#########   selectstudy 윈도우   ##############
form_selectstudy = resource_path(".//ui//selectstudy.ui")
form_selectstudy_class = uic.loadUiType(form_selectstudy)[0]
##############################################

#########   hearstudy 윈도우   ##############
form_hearstudy = resource_path(".//ui//hearstudy.ui")
form_hearstudy_class = uic.loadUiType(form_hearstudy)[0]
##############################################

##############################################################################
class Main(QDialog, QWidget, form_main_class):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_2.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_4.setFont(QtGui.QFont("12롯데마트드림Bold", 10))
        self.show()

    def toselectsense(self):
        self.selectsense = Selectsense_window()
        self.selectsense.exec()

    def toselectstudy(self):
        self.selectstudy = Selectstudy_window()
        self.selectstudy.exec()

    def finish(self):
        self.close()
##############################################################################################
class Hearstudy_window(QDialog, QWidget, form_hearstudy_class):
    mysound=''
    list=[]
    list_q=[]
    list_bool=[False,False,False,False,False,False,False,False,False,False]
    count=0
    sound_bool=False
    def __init__(self):
        super(Hearstudy_window, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_6.setFont(QtGui.QFont("12롯데마트드림Bold", 14))
        self.pushButton_7.setEnabled(False)
        self.pushButton_7.setStyleSheet('background : transparent')
        self.pushButton_8.setEnabled(False)
        self.pushButton_8.setStyleSheet('background : transparent')
        self.pushButton_9.setEnabled(False)
        self.pushButton_9.setStyleSheet('background : transparent')

        path = ".//question//sound.csv"
        question = pd.read_csv(path, encoding='cp949')
        ran_num = random.randint(0, 29)

        for i in range(10):
            while ran_num in self.list:
                ran_num = random.randint(0, 9)
            self.list.append(ran_num)
            self.list_q.append([question['answer'][ran_num], question['a1'][ran_num], question['a2'][ran_num],
                           question['a3'][ran_num], question['a4'][ran_num], question['filename'][ran_num]])

        self.label_5.setText("Q1. 다음 소리를 듣고 해당하는 답을 고르세요.")
        self.pushButton_2.setText("1번 "+self.list_q[self.count][1])
        self.pushButton_4.setText("2번 " + self.list_q[self.count][2])
        self.pushButton_5.setText("3번 " + self.list_q[self.count][3])
        self.pushButton_6.setText("4번 " + self.list_q[self.count][4])

        pygame.init()
        self.mysound = pygame.mixer.Sound(".//hearsound//" + self.list_q[self.count][5])


    def toSelectstudy(self):
        self.close()

    def backQ(self):
        self.count = self.count - 1
        pygame.init()
        self.mysound = pygame.mixer.Sound(".//hearsound//" + self.list_q[self.count][5])
        if(self.count==0):
            self.pushButton_8.setEnabled(False)
            self.pushButton_8.setStyleSheet('background : transparent')


        if (self.list_bool[self.count] == True):
            self.pushButton_7.setEnabled(True)
        else:
            self.pushButton_7.setEnabled(False)

        if (self.count < 9):
            self.pushButton_7.setEnabled(True)
            self.pushButton_7.setStyleSheet('border-image:url(".//resource//right.png");background : transparent')

        self.label_5.setText("Q" + str(self.count + 1) + ". 다음 소리를 듣고 해당하는 답을 고르세요.")
        self.pushButton_2.setText("1번 " + self.list_q[self.count][1])
        self.pushButton_4.setText("2번 " + self.list_q[self.count][2])
        self.pushButton_5.setText("3번 " + self.list_q[self.count][3])
        self.pushButton_6.setText("4번 " + self.list_q[self.count][4])
        self.label_6.setText("")


    def nextQ(self):
        self.count = self.count + 1
        pygame.init()
        self.mysound = pygame.mixer.Sound(".//hearsound//" + self.list_q[self.count][5])
        if(self.list_bool[self.count]==True):
            self.pushButton_7.setEnabled(True)
        else:
            self.pushButton_7.setEnabled(False)

        if(self.count==9):
            self.pushButton_7.setEnabled(False)
            self.pushButton_7.setStyleSheet('background : transparent')

        if(self.count>0):
            self.pushButton_8.setEnabled(True)
            self.pushButton_8.setStyleSheet('border-image:url(".//resource//left.png");background : transparent')

        self.label_5.setText("Q"+str(self.count+1)+". 다음 소리를 듣고 해당하는 답을 고르세요.")
        self.pushButton_2.setText("1번 " + self.list_q[self.count][1])
        self.pushButton_4.setText("2번 " + self.list_q[self.count][2])
        self.pushButton_5.setText("3번 " + self.list_q[self.count][3])
        self.pushButton_6.setText("4번 " + self.list_q[self.count][4])
        self.label_6.setText("")


    def q1(self):
        if((self.list_q[self.count][0] == 1) and self.count<9):
            self.pushButton_7.setEnabled(True)
            self.pushButton_7.setStyleSheet('border-image:url(".//resource//right.png");background : transparent')
            self.list_bool[self.count]=True
            self.label_6.setText("정답입니다. 다음 문제로 이동해주세요.")
        elif(self.count<9):
            self.label_6.setText("1번은 오답입니다.")

        if ((self.list_q[self.count][0] == 1) and self.count==9):
            self.pushButton_9.setEnabled(True)
            self.label_6.setText("정답입니다. 10문제를 모두 푸셨습니다.")
            self.pushButton_9.setStyleSheet('border-style:solid;border-color:rgb(0,101,51);border-width:2px;border-radius:3px;background : transparent')
            self.pushButton_9.setText("퀴즈 종료하기")
        elif (self.count == 9):
            self.label_6.setText("1번은 오답입니다.")


    def q2(self):
        if ((self.list_q[self.count][0] == 2) and self.count<9):
            self.pushButton_7.setEnabled(True)
            self.pushButton_7.setStyleSheet('border-image:url(".//resource//right.png");background : transparent')
            self.list_bool[self.count] = True
            self.label_6.setText("정답입니다. 다음 문제로 이동해주세요.")

        elif(self.count<9):
            self.label_6.setText("2번은 오답입니다.")

        if ((self.list_q[self.count][0] == 2) and self.count==9):
            self.pushButton_9.setEnabled(True)
            self.label_6.setText("정답입니다. 10문제를 모두 푸셨습니다.")
            self.pushButton_9.setStyleSheet('border-style:solid;border-color:rgb(0,101,51);border-width:2px;border-radius:3px;background : transparent')
            self.pushButton_9.setText("퀴즈 종료하기")
        elif (self.count == 9):
            self.label_6.setText("2번은 오답입니다.")

    def q3(self):
        if ((self.list_q[self.count][0] == 3) and self.count<9):
            self.pushButton_7.setEnabled(True)
            self.pushButton_7.setStyleSheet('border-image:url(".//resource//right.png");background : transparent')
            self.list_bool[self.count] = True
            self.label_6.setText("정답입니다. 다음 문제로 이동해주세요.")

        elif(self.count<9):
            self.label_6.setText("3번은 오답입니다.")

        if ((self.list_q[self.count][0] == 3) and self.count==9):
            self.pushButton_9.setEnabled(True)
            self.label_6.setText("정답입니다. 10문제를 모두 푸셨습니다.")
            self.pushButton_9.setStyleSheet('border-style:solid;border-color:rgb(0,101,51);border-width:2px;border-radius:3px;background : transparent')
            self.pushButton_9.setText("퀴즈 종료하기")
        elif (self.count == 9):
            self.label_6.setText("3번은 오답입니다.")

    def q4(self):
        if ((self.list_q[self.count][0] == 4) and self.count<9):
            self.pushButton_7.setEnabled(True)
            self.pushButton_7.setStyleSheet('border-image:url(".//resource//right.png");background : transparent')
            self.list_bool[self.count] = True
            self.label_6.setText("정답입니다. 다음 문제로 이동해주세요.")

        elif(self.count<9):
            self.label_6.setText("4번은 오답입니다.")

        if ((self.list_q[self.count][0] == 4) and self.count==9):
            self.pushButton_9.setEnabled(True)
            self.label_6.setText("정답입니다. 10문제를 모두 푸셨습니다.")
            self.pushButton_9.setStyleSheet('border-style:solid;border-color:rgb(0,101,51);border-width:2px;border-radius:3px;background : transparent')
            self.pushButton_9.setText("퀴즈 종료하기")
        elif(self.count==9):
            self.label_6.setText("4번은 오답입니다.")

    def finish(self):
        self.close()

    def soundplay(self):
        if (self.sound_bool == False):
            self.pushButton.setStyleSheet('border-image:url(".//resource//stopbutton.png");background : transparent')
            self.sound_bool = True
            self.mysound.play()
            self.sound_bool = False
        else:
            self.pushButton.setStyleSheet('border-image:url(".//resource//playbutton.png");background : transparent')
            self.sound_bool = False
            self.mysound.stop()











#############################################################################
#############################################################################
class Selectstudy_window(QDialog, QWidget, form_selectstudy_class):
    def __init__(self):
        super(Selectstudy_window, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_6.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_7.setFont(QtGui.QFont("12롯데마트드림Bold", 18))

    def toMain(self):
        self.close()

    def toenvironment(self):
        pass

    def toemotion(self):
        pass

    def tosound(self):
        self.hearstudy = Hearstudy_window()
        self.hearstudy.exec()


#############################################################################
class Selectsense_window(QDialog, QWidget, form_trainselect_class):
    def __init__(self):
        super(Selectsense_window, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_2.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_6.setFont(QtGui.QFont("12롯데마트드림Bold", 18))

    def toMain(self):
        self.close()

    def todefault(self):
        self.default = Default_window()
        self.default.exec()

    def tosiren(self):
        self.siren = Siren_window()
        self.siren.exec()

    def tobabycry(self):
        self.siren = Babycry_window()
        self.siren.exec()

    def toscream(self):
        self.scream = Scream_window()
        self.scream.exec()

###########################################################################
class Default_window(QDialog, QWidget, form_nowtrain_class):
    threadbool=False
    def __init__(self):
        super(Default_window, self).__init__()
        self.initUI()
        self.show()



    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_5.setText("실행 버튼을 누르면 기본 감지 모드가 실행됩니다.")


    def toSelectsense(self):
        if(self.threadbool==True):
            self.worker.stop()
        self.close()

    def sensestart(self):
        self.worker = Aiworker()
        self.worker.start()
        self.label_5.setText("기본 감지 모드가 실행 중 입니다.")
        self.threadbool=True
        self.worker.putimage.connect(self.putimage)
        self.pushButton.setEnabled(False)
        self.pushButton.setStyleSheet('border-image:url(".//resource//gamzi.png");border:0px;')




    def putimage(self, what,image):
        self.label_5.setText(what)
        self.pushButton.setStyleSheet("border-image:url("+image+");border:0px;")

    def sensestop(self):
        quit_msg = "소리감지 기능을 종료하시겠습니까?"
        reply=QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if self.threadbool==True and reply == QMessageBox.Yes:
            self.worker.stop()
            self.defaultwindow = Default_window()
            self.close()
            self.defaultwindow.exec()





###########################################################################
class Siren_window(QDialog, QWidget, form_nowtrain_class):
    threadbool = False

    def __init__(self):
        super(Siren_window, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_5.setText("실행 버튼을 누르면 사이렌 감지 모드가 실행됩니다.")

    def toSelectsense(self):
        if (self.threadbool == True):
            self.worker.stop()
        self.close()

    def sensestart(self):
        self.worker = Aiworker_2()
        self.worker.start()
        self.label_5.setText("사이렌 감지 모드가 실행 중 입니다.")
        self.threadbool = True
        self.worker.putimage.connect(self.putimage)
        self.pushButton.setEnabled(False)
        self.pushButton.setStyleSheet('border-image:url(".//resource//gamzi.png");border:0px;')

    def putimage(self, what, image):
        self.label_5.setText(what)
        self.pushButton.setStyleSheet("border-image:url(" + image + ");border:0px;")

    def sensestop(self):
        quit_msg = "소리감지 기능을 종료하시겠습니까?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if self.threadbool == True and reply == QMessageBox.Yes:
            self.worker.stop()
            self.defaultwindow = Default_window()
            self.close()
            self.defaultwindow.exec()

#############################################################################
class Babycry_window(QDialog, QWidget, form_nowtrain_class):
    threadbool = False

    def __init__(self):
        super(Babycry_window, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_5.setText("실행 버튼을 누르면 아기울음소리 감지 모드가 실행됩니다.")

    def toSelectsense(self):
        if (self.threadbool == True):
            self.worker.stop()
        self.close()

    def sensestart(self):
        self.worker = Aiworker_3()
        self.worker.start()
        self.label_5.setText("아기울음소리 감지 모드가 실행 중 입니다.")
        self.threadbool = True
        self.worker.putimage.connect(self.putimage)
        self.pushButton.setEnabled(False)
        self.pushButton.setStyleSheet('border-image:url(".//resource//gamzi.png");border:0px;')

    def putimage(self, what, image):
        self.label_5.setText(what)
        self.pushButton.setStyleSheet("border-image:url(" + image + ");border:0px;")

    def sensestop(self):
        quit_msg = "소리감지 기능을 종료하시겠습니까?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if self.threadbool == True and reply == QMessageBox.Yes:
            self.worker.stop()
            self.defaultwindow = Default_window()
            self.close()
            self.defaultwindow.exec()

#############################################################################
class Scream_window(QDialog, QWidget, form_nowtrain_class):
    threadbool = False

    def __init__(self):
        super(Scream_window, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_5.setText("실행 버튼을 누르면 비명 감지 모드가 실행됩니다.")

    def toSelectsense(self):
        if (self.threadbool == True):
            self.worker.stop()
        self.close()

    def sensestart(self):
        self.worker = Aiworker_4()
        self.worker.start()
        self.label_5.setText("비명 감지 모드가 실행 중 입니다.")
        self.threadbool = True
        self.worker.putimage.connect(self.putimage)
        self.pushButton.setEnabled(False)
        self.pushButton.setStyleSheet('border-image:url(".//resource//gamzi.png");border:0px;')

    def putimage(self, what, image):
        self.label_5.setText(what)
        self.pushButton.setStyleSheet("border-image:url(" + image + ");border:0px;")

    def sensestop(self):
        quit_msg = "소리감지 기능을 종료하시겠습니까?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if self.threadbool == True and reply == QMessageBox.Yes:
            self.worker.stop()
            self.defaultwindow = Default_window()
            self.close()
            self.defaultwindow.exec()

########### 기본 감지 인공지능 백그라운드 실행 ############################
class Aiworker(QThread):
    putimage = pyqtSignal(str,str)

    max_pad_len = 87
    num_rows = 40
    num_columns = 87
    num_channels = 1
    default_model = load_model(".//models//default_mfcc.h5")
    def __init__(self):
        super().__init__()
        self.power=True

    def run(self):
        while self.power:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            RECORD_SECONDS = 2
            WAVE_OUTPUT_FILENAME = "./this.wav"

            p= pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate = RATE,input=True, frames_per_buffer=CHUNK)   #요기가 지금 안됌
            print("* recording")

            frames=[]

            for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("*done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()
            wf=wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            filename='this.wav'
            answer = self.print_prediction(filename)
            if (answer == 0):  # babycry
                print("babycry")
                self.putimage.emit("아기 울음소리", ".//resource//babycryim.png")
                time.sleep(5.0)
            elif (answer == 1):  # carhorn
                print("test1")
                self.putimage.emit("경적 소리", ".//resource//horn.png")
                time.sleep(5.0)
            elif (answer == 2):  # dogbark
                print("test2")
                self.putimage.emit("개 짖는 소리",".//resource//dog.png")
                time.sleep(5.0)
            elif (answer == 3):  # glassbreak
                print("test3")
                self.putimage.emit("유리 깨지는 소리",".//resource//breakglass.png")
                time.sleep(5.0)
            elif (answer == 4):  # knock
                print("test4")
                self.putimage.emit("노크 소리",".//resource//knock.png")
                time.sleep(5.0)
            elif (answer == 5):  # meow
                print("test5")
                self.putimage.emit("고양이 울음소리", ".//resource//moew.png")
                time.sleep(5.0)
            elif (answer == 6):  # scream
                print("test6")
                self.putimage.emit("비명 소리", ".//resource//screamim.png")
                time.sleep(5.0)
            elif (answer == 7):  # siren
                print("test7")
                self.putimage.emit("사이렌 소리", ".//resource//sirenim.png")
                time.sleep(5.0)
            elif (answer == 10):
                self.putimage.emit("기본 감지 모드가 실행 중 입니다.", ".//resource//gamzi.png")

    def stop(self):
        self.power=False
        self.quit()
        self.wait(3000)
        time.sleep(2.0)


    ################## 특징 추출 함수 ######################

    def mfcc_extraction(self, file_name):

        try:
            audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            pad_width = self.max_pad_len - mfccs.shape[1]
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')

        except Exception as e:
            print("Error 발생: ", file_name)
            return None

        return mfccs

    ################## 추론하는 함수 #####################

    def print_prediction(self, file_name):
        prediction_feature = self.mfcc_extraction(file_name)
        prediction_feature = prediction_feature.reshape(1, self.num_rows, self.num_columns, self.num_channels)
        y_prob = self.default_model.predict(prediction_feature)
        predicted_vector = y_prob.argmax(axis=-1)  # predicter_vector가 가장 높은 클래스
        predicted_proba_vector = self.default_model.predict(prediction_feature)
        predicted_proba = predicted_proba_vector[0]  # 정확도 추출
        if (predicted_proba[predicted_vector]<0.99):  # 가장 정확도 높은 클래스의 정확도 실수값
            return 10
        return predicted_vector

###################################################################################################################
###################################################################################################################
########### 사이렌 감지 인공지능 백그라운드 실행 ############################
class Aiworker_2(QThread):
    putimage = pyqtSignal(str,str)

    max_pad_len = 87
    num_rows = 40
    num_columns = 87
    num_channels = 1
    default_model = load_model(".//models//siren_mfcc.h5")
    def __init__(self):
        super().__init__()
        self.power=True

    def run(self):
        while self.power:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            RECORD_SECONDS = 2
            WAVE_OUTPUT_FILENAME = "./this.wav"

            p= pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate = RATE,input=True, frames_per_buffer=CHUNK)   #요기가 지금 안됌
            print("* recording")

            frames=[]

            for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("*done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()
            wf=wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            filename='this.wav'
            answer = self.print_prediction(filename)
            if (answer == 0):  # burglar_alarm
                print("burglar_alarm")
                self.putimage.emit("도난경보 소리", ".//resource//burglar.png")
                time.sleep(5.0)
            elif (answer == 1):  # emergency_alarm
                print("emergency_alarm")
                self.putimage.emit("응급경보 소리", ".//resource//emergency.png")
                time.sleep(5.0)
            elif (answer == 2):  # fire_alarm
                print("fire_alarm")
                self.putimage.emit("화재경보 소리",".//resource//fire.png")
                time.sleep(5.0)
            elif (answer == 3):  # other
                print("other")
                self.putimage.emit("사이렌 감지 모드가 실행 중 입니다.",".//resource//gamzi.png")
                time.sleep(1.0)
            elif (answer == 10):  # 0.99미만
                print("0.99미만")
                self.putimage.emit("사이렌 감지 모드가 실행 중 입니다.",".//resource//gamzi.png")
                time.sleep(1.0)

    def stop(self):
        self.power=False
        self.quit()
        self.wait(3000)
        time.sleep(2.0)


    ################## 특징 추출 함수 ######################

    def mfcc_extraction(self, file_name):

        try:
            audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            pad_width = self.max_pad_len - mfccs.shape[1]
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')

        except Exception as e:
            print("Error 발생: ", file_name)
            return None

        return mfccs

    ################## 추론하는 함수 #####################

    def print_prediction(self, file_name):
        prediction_feature = self.mfcc_extraction(file_name)
        prediction_feature = prediction_feature.reshape(1, self.num_rows, self.num_columns, self.num_channels)
        y_prob = self.default_model.predict(prediction_feature)
        predicted_vector = y_prob.argmax(axis=-1)  # predicter_vector가 가장 높은 클래스
        predicted_proba_vector = self.default_model.predict(prediction_feature)
        predicted_proba = predicted_proba_vector[0]  # 정확도 추출
        if (predicted_proba[predicted_vector]<0.99):  # 가장 정확도 높은 클래스의 정확도 실수값
            return 10
        return predicted_vector


######################################################################################################################
########### 아기울음소리 감지 인공지능 백그라운드 실행 ############################
class Aiworker_3(QThread):
    putimage = pyqtSignal(str,str)

    max_pad_len = 87
    num_rows = 40
    num_columns = 87
    num_channels = 1
    default_model = load_model(".//models//babycry_mfcc.h5")
    def __init__(self):
        super().__init__()
        self.power=True

    def run(self):
        while self.power:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            RECORD_SECONDS = 2
            WAVE_OUTPUT_FILENAME = "./this.wav"

            p= pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate = RATE,input=True, frames_per_buffer=CHUNK)
            print("* recording")

            frames=[]

            for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("*done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()
            wf=wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            filename='this.wav'
            answer = self.print_prediction(filename)
            if (answer == 0):  # babycry
                print("babycry")
                self.putimage.emit("아기울음 소리", ".//resource//babycryim.png")
                time.sleep(5.0)
            elif (answer == 1):  # other
                print("other")
                self.putimage.emit("아기울음소리 감지 모드가 실행 중 입니다.", ".//resource//gamzi.png")
                time.sleep(1.0)
            elif (answer == 10):  # 0.99미만
                print("0.99미만")
                self.putimage.emit("아기울음소리 감지 모드가 실행 중 입니다.",".//resource//gamzi.png")
                time.sleep(1.0)

    def stop(self):
        self.power=False
        self.quit()
        self.wait(3000)
        time.sleep(2.0)


    ################## 특징 추출 함수 ######################

    def mfcc_extraction(self, file_name):

        try:
            audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            pad_width = self.max_pad_len - mfccs.shape[1]
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')

        except Exception as e:
            print("Error 발생: ", file_name)
            return None

        return mfccs

    ################## 추론하는 함수 #####################

    def print_prediction(self, file_name):
        prediction_feature = self.mfcc_extraction(file_name)
        prediction_feature = prediction_feature.reshape(1, self.num_rows, self.num_columns, self.num_channels)
        y_prob = self.default_model.predict(prediction_feature)
        predicted_vector = y_prob.argmax(axis=-1)  # predicter_vector가 가장 높은 클래스
        predicted_proba_vector = self.default_model.predict(prediction_feature)
        predicted_proba = predicted_proba_vector[0]  # 정확도 추출
        if (predicted_proba[predicted_vector]<0.95):  # 가장 정확도 높은 클래스의 정확도 실수값
            return 10
        return predicted_vector


######################################################################################################################
########### 비명 감지 인공지능 백그라운드 실행 ############################
class Aiworker_4(QThread):
    putimage = pyqtSignal(str,str)

    max_pad_len = 87
    num_rows = 40
    num_columns = 87
    num_channels = 1
    default_model = load_model(".//models//scream_mfcc.h5")
    def __init__(self):
        super().__init__()
        self.power=True

    def run(self):
        while self.power:
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 44100
            RECORD_SECONDS = 2
            WAVE_OUTPUT_FILENAME = "./this.wav"

            p= pyaudio.PyAudio()
            stream = p.open(format=FORMAT, channels=CHANNELS, rate = RATE,input=True, frames_per_buffer=CHUNK)
            print("* recording")

            frames=[]

            for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("*done recording")

            stream.stop_stream()
            stream.close()
            p.terminate()
            wf=wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            filename='this.wav'
            answer = self.print_prediction(filename)
            if (answer == 0):  # other
                print("other")
                self.putimage.emit("비명 감지 모드가 실행 중 입니다.", ".//resource//gamzi.png")
                time.sleep(1.0)
            elif (answer == 1):  # scream
                print("scream")
                self.putimage.emit("비명 소리", ".//resource//screamim.png")
                time.sleep(1.0)
            elif (answer == 10):  # 0.90미만
                print("0.90미만")
                self.putimage.emit("비명 감지 모드가 실행 중 입니다.",".//resource//gamzi.png")
                time.sleep(1.0)

    def stop(self):
        self.power=False
        self.quit()
        self.wait(3000)
        time.sleep(2.0)


    ################## 특징 추출 함수 ######################

    def mfcc_extraction(self, file_name):

        try:
            audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
            mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
            pad_width = self.max_pad_len - mfccs.shape[1]
            mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')

        except Exception as e:
            print("Error 발생: ", file_name)
            return None

        return mfccs

    ################## 추론하는 함수 #####################

    def print_prediction(self, file_name):
        prediction_feature = self.mfcc_extraction(file_name)
        prediction_feature = prediction_feature.reshape(1, self.num_rows, self.num_columns, self.num_channels)
        y_prob = self.default_model.predict(prediction_feature)
        predicted_vector = y_prob.argmax(axis=-1)  # predicter_vector가 가장 높은 클래스
        predicted_proba_vector = self.default_model.predict(prediction_feature)
        predicted_proba = predicted_proba_vector[0]  # 정확도 추출
        if (predicted_proba[predicted_vector]<0.90):  # 가장 정확도 높은 클래스의 정확도 실수값
            return 10
        return predicted_vector


######################################################################################################################





########################################################################################################################
if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('.//resource//12롯데마트드림Bold.ttf')
    app.setFont(QFont('12롯데마트드림Bold'))
    ex = Main()
    ex.show()
    sys.exit(app.exec_())