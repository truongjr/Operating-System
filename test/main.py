import sys
from gtts import gTTS
from PyQt5.QtWidgets import*
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from UI import Ui_MainWindow

count = 0


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.player = QMediaPlayer()
        self.uic.playButton.clicked.connect(self.Read)
        self.uic.pauseButton.clicked.connect(self.Pause)
        self.uic.chooseFileButton.clicked.connect(self.ChooseFile)

    def show(self):
        self.main_win.show()

    def Read(self):
        global count
        text = self.uic.textEdit.toPlainText()
        idx = self.uic.selectLang.currentIndex()
        if idx == 0:
            if len(text) == 0:
                text = "Hãy nhập văn bản"
            tts = gTTS(text=text, lang='vi')
        else:
            if len(text) == 0:
                text = "Please enter text"
            tts = gTTS(text=text, lang='en')
        tts.save(f'speech{count % 2}.mp3')
        file_path = "C:\\Users\\nguye\\PycharmProjects\\test\\" + f'speech{count % 2}.mp3'
        url = QUrl.fromLocalFile(file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
        count += 1

    def Pause(self):
        self.player.pause()

    def ChooseFile(self):
        res = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Open file',
            directory='C:\\Users\\nguye\\PycharmProjects\\test',
            filter='Text file (*.txt *.mp3 *.doc *docx);;Sound file (*.mp3)',
        )
        file_path = str(res[0])[2:-2]
        file_name = str(file_path).split('/')[-1]
        file_format = file_name.split('.')[-1]
        if file_format == 'txt' or file_format == 'doc' or file_format == 'docx':
            file_content = str(open(file_name, 'r', encoding='utf-8').read())
            self.uic.textEdit.clear()
            self.uic.textEdit.setText(file_content)
            # print(file_content)
        elif file_format == 'mp3':
            url = QUrl.fromLocalFile(file_path)
            content = QMediaContent(url)
            self.player.setMedia(content)
            self.player.play()

        # print(file_path, file_name, file_format)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
