import humanize
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import os.path
from PyQt5.uic import loadUiType
import urllib.request
from pafy import *

ui, _ = loadUiType('D:/backup/Desktop/DeskFiles/pydesign/main.ui')

class mainApp(QMainWindow, ui):

    def __init__(self, parent=None):
        super(mainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.IniUI()
        self.handelButtons()

    def IniUI(self):
        # contain all ui changes in loading
        # self.tabWidget.tabBar().setVisible(False)
        self.animation()
        pass

    def handelButtons(self):
        # handel all buttons in tha app
        self.downloadOther.clicked.connect(self.download)
        self.borwseOther.clicked.connect(self.handelBrowse)
        self.gitsingledata.clicked.connect(self.getVideoDate)
        self.singleb.clicked.connect(self.saveBrowes)
        self.singleD.clicked.connect(self.DownloadVideo)
        self.playB.clicked.connect(self.playbrowse)
        self.playD.clicked.connect(self.downloadPlayList)
        self.home.clicked.connect(self.gohome)
        self.home.clicked.connect(self.animation)
        self.down.clicked.connect(self.godown)
        self.you.clicked.connect(self.goyou)
        self.setting.clicked.connect(self.gosetting)
        self.pushButton_2.clicked.connect(self.dark)
        self.pushButton.clicked.connect(self.defaul)
        self.pushButton_3.clicked.connect(self.blue)
        # pass

    def handelProgressBar(self, blocnum, blocksize, totalsize):
        readedData = blocnum*blocksize
        if totalsize > 0:
            downloadPercentage = readedData*100/totalsize
            self.OtherprogressBar.setValue(downloadPercentage)
            QApplication.processEvents()
        # calculate the progressing
        # pass

    def handelBrowse(self):
        saveLocation = QFileDialog.getSaveFileName(
            self, caption="save as", directory=".", filter="all files(*.*)")
        self.otherLocation.setText(str(saveLocation[0]))
        # pick save location
        # pass

    def download(self):
        # print(1)
        url = self.otherUrl.text()
        saveLocation = self.otherLocation.text()
        if url == "" or saveLocation == "":
            # self.errormsg.setText("there is no url or location")
            QMessageBox.warning(
                self, "Error", "there is no url or location please enter the url and save location")
        else:
            try:
                urllib.request.urlretrieve(
                    url, saveLocation, self.handelProgressBar)
        # pass
            except Exception:
                QMessageBox.warning(self, "Download Error", "Un_vaild url")
                return
        QMessageBox.information(
            self, "Download Compelete", "The Download Compelete Successfully")
        self.OtherprogressBar.setValue(0)
        self.otherUrl.setText("")
        self.otherLocation.setText("")

    def saveBrowes(self):
        #  save location on line edit

        pass

#  youtube download single video
    def saveBrowes(self):
        #  save location on line edit
        saveLocation = QFileDialog.getSaveFileName(
            self, caption="save as", directory=".", filter="all files(*.*)")
        self.singlelocation.setText(str(saveLocation[0]))

        # pass

    def getVideoDate(self):

        videourl = self.singleurl.text()
        videoSaveLocation = self.singlelocation.text()

        if videourl == "" or videoSaveLocation == "":
            QMessageBox.warning(
                self, "Error", "there is no url or location please enter the url and save location")
        else:
            video = pafy.new(videourl)
            print(video.title)
            print(video.duration)
            video_qulaity = video.videostreams
            for q in video_qulaity:
                size = humanize.naturalsize(q.get_filesize())
                data = "{} {} {} {}".format(
                    q.mediatype, q.extension, q.quality, size)
                self.singlecombo.addItem(data)
        # pass

    def DownloadVideo(self):
        print("here")
        video_url_s = self.singleurl.text()
        save_location_s = self.singlelocation.text()
        if video_url_s == "" or save_location_s == "":
            # self.errormsg.setText("there is no url or location")
            QMessageBox.warning(
                self, "Error", "there is no url or location please enter the url and save location")
        else:
            video = pafy.new(video_url_s)
            videostream = video.videostreams
            print(videostream)
            videoquality = self.singlecombo.currentIndex()
            print(videoquality)
            download = videostream[videoquality].download(
                filepath=save_location_s, callback=self.videoPROGRESS)
            try:

                urllib.request.urlretrieve(
                    video_url_s, save_location_s, self.handelProgressBar)
                QMessageBox.information(
                    self, "Download Compelete", "The Download Compelete Successfully")
                self.singlecombo.clear()
        # pass
            except Exception:
                QMessageBox.warning(self, "Download Error", "Un_vaild url")
                return
        self.singlebar.setValue(0)
        self.singleurl.setText("")
        self.singlelocation.setText("")
        self.downloaded.setText("")
        self.rate.setText("")
        self.time.setText("")

        # pass

    def videoPROGRESS(self, total, received, ratio, rate, time):
        if total > 0:
            self.singlebar.setValue(ratio*100)
            self.downloaded.setText(
                str("Downloaded : {}".format(humanize.naturalsize(received))))
            self.rate.setText(
                str("Rate : {}".format(humanize.naturalsize(rate))))
            self.time.setText(
                str("Time remaining : {}".format((time))))
            QApplication.processEvents()

        # pass

    #  youtube playlist

    def downloadPlayList(self):
        urlp = self.playurl.text()
        location = self.playloc.text()
        if urlp == "" or location == "":
            QMessageBox.warning(
                self, "Error", "there is no url or location please enter the url and save location")
        else:
            import pafy
            playlistt = pafy.get_playlist(urlp)
            self.lcdNumber_2.display(len(playlistt['items']))

            os.chdir(location)
            if os.path.exists(str(playlistt['title'])):
                os.chdir(str(playlistt['title']))
            else:
                os.mkdir(str(playlistt['title']))
                os.chdir(str(playlistt['title']))
            current_video_in_download = 0
            qulaityplaylist = self.playquality.currentIndex()
            self.lcdNumber.display(current_video_in_download)
            self.lcdNumber_3.display(
                len(playlistt['items'])-current_video_in_download)

            for v in playlistt['items']:
                current_video = v['pafy']
                current_stream = current_video.videostreams
                download = current_stream[qulaityplaylist].download(
                    callback=self.playprogress)
                current_video_in_download += 1
                self.lcdNumber.display(current_video_in_download)
                self.lcdNumber_3.display(
                    len(playlistt['items'])-current_video_in_download)
            QMessageBox.information(
                self, 'Compelete', "Download Compelet successfuly")
            self.lcdNumber.display(0)
            self.lcdNumber_2.display(0)
            self.lcdNumber_3.display(0)
            self.playurl.setText("")
            self.playloc.setText("")
            self.playbar.setValue(0)
            self.label_4.setText("")
            self.label_5.setText("")
            self.label_6.setText("")

    def playprogress(self, total, received, ratio, rate, time):
        if total > 0:
            self.playbar.setValue(ratio*100)
            self.label_4.setText(
                str("Downloaded : {}".format(humanize.naturalsize(received))))
            self.label_5.setText(
                str("Rate : {}".format(humanize.naturalsize(rate))))
            self.label_6.setText(
                str("Time remaining : {}".format((time))))
            QApplication.processEvents()
        # pass

    def playbrowse(self):
        se = QFileDialog().getExistingDirectory()
        self.playloc.setText(str(se))

    def gohome(self):
        self.tabWidget.setCurrentIndex(0)

    def godown(self):
        self.tabWidget.setCurrentIndex(1)

    def goyou(self):
        self.tabWidget.setCurrentIndex(2)

    def gosetting(self):
        self.tabWidget.setCurrentIndex(3)

    def dark(self):
        style = open('D:/backup/Desktop/DeskFiles/pydesign/themes/dark.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def blue(self):
        style = open('D:/backup/Desktop/DeskFiles/pydesign/themes/blue.css', 'r')
        style = style.read()
        self.setStyleSheet(style)

    def defaul(self):
        self.setStyleSheet(None)

    def animation(self):
        box1 = QPropertyAnimation(self.groupBox, b"geometry")
        box1.setDuration(1000)
        box1.setStartValue(QRect(0, 0, 0, 0))
        box1.setEndValue(QRect(60, 40, 271, 181))
        box1.start()
        self.box1 = box1

        box2 = QPropertyAnimation(self.groupBox_2, b"geometry")
        box2.setDuration(1000)
        box2.setStartValue(QRect(760, -160, 0, 0))
        box2.setEndValue(QRect(420, 40, 271, 181))
        box2.start()
        self.box2 = box2

        box3 = QPropertyAnimation(self.groupBox_3, b"geometry")
        box3.setDuration(1000)
        box3.setStartValue(QRect(-250, 470, 0, 0))
        box3.setEndValue(QRect(60, 290, 271, 181))
        box3.start()
        self.box3 = box3

        box4 = QPropertyAnimation(self.groupBox_4, b"geometry")
        box4.setDuration(1000)
        box4.setStartValue(QRect(730, 470, 0, 0))
        box4.setEndValue(QRect(420, 290, 271, 181))
        box4.start()
        self.box4 = box4


def main():
    app = QApplication(sys.argv)
    window = mainApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
