import sys
import os
import time

import pyaudio
import wave
import librosa
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QFontDatabase,QMovie

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

    def finish(self):
        self.close()

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
        self.close()

#############################################################################
class Babycry_window(QDialog, QWidget, form_nowtrain_class):
    def __init__(self):
        super(Babycry_window, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))
        self.label_5.setText("실행 버튼을 누르면 아기울음 감지 모드가 실행됩니다.")

    def toSelectsense(self):
        self.close()

#############################################################################
class Scream_window(QDialog, QWidget, form_nowtrain_class):
    def __init__(self):
        super(Scream_window, self).__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setupUi(self)
        self.setWindowFlag((QtCore.Qt.FramelessWindowHint))
        self.label_5.setFont(QtGui.QFont("12롯데마트드림Bold", 18))

    def toSelectsense(self):
        self.close()

########### 인공지능 백그라운드 실행 ############################
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('.//resource//12롯데마트드림Bold.ttf')
    app.setFont(QFont('12롯데마트드림Bold'))
    ex = Main()
    ex.show()
    sys.exit(app.exec_())