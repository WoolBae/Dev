import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, pyqtSignal,QUrl
import re
from lib.AuthDialog import AuthDialog
import datetime
from lib.YouViewrLayout import Ui_MainWindow



#
# form_class = uic.loadUiType("c:/section6/ui/you_viwer_v1.0.ui")[0]

class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        #초기화
        self.setupUi(self)
        # 초기 잠금
        self.initAuthLock()
        # 시그널 초기화
        self.initSignal()
        # 로그인 관련 변수 선언
        self.user_id  =None
        self.user_pw = None

        #재생 여부
        self.is_play = False




        #기본 UI비활성화
    def initAuthLock(self):
        self.previewButton.setEnabled(False)
        self.fileNavButton.setEnabled(False)
        self.streamCombobox.setEnabled(False)
        self.startButton.setEnabled(False)
        self.calendarWidget.setEnabled(False)
        self.urlTextEdit.setEnabled(False)
        self.pathTextEdit.setEnabled(False)
        self.showStatusMsg('인증안됨')

    #기본 UI비활성화
    def initAuthActive(self):
        self.previewButton.setEnabled(True)
        self.fileNavButton.setEnabled(True)
        self.streamCombobox.setEnabled(True)
        self.calendarWidget.setEnabled(True)
        self.urlTextEdit.setEnabled(True)
        self.pathTextEdit.setEnabled(True)
        self.showStatusMsg('인증 완료')

    def showStatusMsg(self, msg):
        self.statusbar.showMessage(msg)

    def initSignal(self):
        self.loginButton.clicked.connect(self.authCheck)
        self.previewButton.clicked.connect(self.load_url)
        self.exitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.webView.loadProgress.connect(self.showProgressBrowserLoading)
        self.fileNavButton.clicked.connect(self.selectDownPath)
        self.calendarWidget.clicked.connect(self.append_date)
    def authCheck(self):
        dlg = AuthDialog()
        dlg.exec_()
        self.user_id = dlg.user_id
        self.user_pw = dlg.user_pw


        if True:
            self.initAuthActive()
            self.loginButton.setText("인증완료")
            self.loginButton.setEnabled(False)
            self.urlTextEdit.setFocus(True)
            self.append_log_msg('login Sucess')

        else:
            QMessageBox.about(self, "인증오류",'아이 또는 비밀번호 인증 오류')


    def load_url(self):
        url = self.urlTextEdit.text().strip()
        v = re.compile('^https://www.youtube.com/?')
        if self.is_play:
            self.append_log_msg('Stop Clik')
            self.webView.load(QUrl('about:blank'))
            self.previewButton.setText('재생')
            self.is_play = False
            self.urlTextEdit.clear()
            self.urlTextEdit.setFocus(True)
            self.startButton.setEnabled(False)
            self.progressBar_2.setValue(0)
            self.showStatusMsg('인증완료')
        else:
            if v.match(url) is not None:
                self.append_log_msg('Play Clik')
                self.webView.load(QUrl(url))
                self.showStatusMsg(url + "재생중")
                self.previewButton.setText('중지')
                self.is_play = True
                self.startButton.setEnabled(True)
            else:
                QMessageBox.about(self,"URL 형식오류","Youtube 주소형식이 아닙니다.")
                self.urlTextEdit.clear()
                self.urlTextEdit.setFocus(True)





    def append_log_msg(self,act):
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
        app_msg = self.user_id + ":" + act +'- ('+ nowDatetime+')'
        print(app_msg)
        self.plainTextEdit.appendPlainText(app_msg)

        #활동 로그 저장 (텍스트 또는 DB)
        with open('c:/section6/log/log.txt','a') as f:
            f.write(app_msg+'\n')

    @pyqtSlot(int)
    def showProgressBrowserLoading(self,v):
        self.progressBar.setValue(v)

    @pyqtSlot()
    def selectDownPath(self):
        #파일선택
        # fname = QFileDialog.getOpenFileName(self)

        fpath = QFileDialog.getExistingDirectory(self,'select Directory')
        self.pathTextEdit.setText(fpath)


    def append_date(self):
        cur_date = self.calendarWidget.selectedDate()
        # print('click date', self.calendarWidget.selectedDate())
        print(str(cur_date.year()) +'-' + str(cur_date.month()) + '-' + str(cur_date.day()))
        self.append_log_msg('calender clik')




        #경로선택

if __name__ == '__main__':
    app = QApplication(sys.argv)
    you_viwer_main = Main()
    you_viwer_main.show()
    app.exec_()
