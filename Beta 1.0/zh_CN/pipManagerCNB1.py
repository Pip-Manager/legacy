from PyQt5.QtWidgets import QWidget, QHBoxLayout, QTableWidget, QPushButton, QApplication, QVBoxLayout, \
    QTableWidgetItem, QMessageBox, QAbstractItemView, QHeaderView, QLabel, QTextEdit, QLineEdit, QDialog
from PyQt5 import QtGui, QtCore
import subprocess
import sys

pipDict = {}


class MainForm(QWidget):
    def __init__(self):
        super(MainForm, self).__init__()
        self.headers = ['编号', '库名', '版本']
        self.setWindowTitle("PIP库管理器 Beta 1.0.0")
        self.setFixedSize(710, 800)
        self.pipFormStatus = 0
        self.pipFormStatusFind = 0

        self.pipList = QTableWidget(self)
        self.controlLabel = QLabel("操作栏:", self)
        self.addButton = QPushButton("添加库", self)
        self.delButton = QPushButton("删除库", self)
        self.findButton = QPushButton("查询库", self)
        self.refreshButton = QPushButton("刷新", self)
        self.aboutButton = QPushButton("关于", self)

        self.button_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        self.all_v_layout.addWidget(self.pipList)
        self.all_v_layout.addWidget(self.controlLabel)
        self.button_h_layout.addWidget(self.addButton)
        self.button_h_layout.addWidget(self.delButton)
        self.button_h_layout.addWidget(self.findButton)
        self.button_h_layout.addWidget(self.refreshButton)
        self.button_h_layout.addWidget(self.aboutButton)
        self.all_v_layout.addLayout(self.button_h_layout)

        self.listInit()
        self.buttonInit()
        self.about_page = AboutPage()
        self.setLayout(self.all_v_layout)

    def addRow(self, pipId, name, ver):
        row = self.pipList.rowCount()
        self.pipList.setRowCount(row + 1)
        newItem = QTableWidgetItem(pipId)
        self.pipList.setItem(row, 0, newItem)
        newItem = QTableWidgetItem(name)
        self.pipList.setItem(row, 1, newItem)
        newItem = QTableWidgetItem(ver)
        self.pipList.setItem(row, 2, newItem)
        self.pipList.setSelectionMode(QAbstractItemView.NoSelection)

    def clearRow(self):
        row = self.pipList.rowCount()
        for i in range(row):
            self.pipList.removeRow(0)

    def startAddTmp(self):
        if self.newLine.text():
            downloadPip = self.newLine.text().strip()
            res = subprocess.Popen("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple " + downloadPip, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
            stderr = str(res.communicate()[1])
            if "No matching distribution found for " in stderr:
                QMessageBox.critical(self, "错误", "未找到库: " + downloadPip, QMessageBox.Yes)
            else:
                QMessageBox.information(self, "操作成功", downloadPip + " 下载成功", QMessageBox.Yes)
            self.newLine.setText("")

    def closeAddTmp(self):
        self.pipFormStatus = 0
        self.newName.deleteLater()
        self.newLine.deleteLater()
        self.startAddButton.deleteLater()
        self.closeAddButton.deleteLater()

    def addPip(self):
        if self.pipFormStatus:
            return
        self.pipFormStatus = 1
        self.newName = QLabel("想要下载的库名称(目前仅支持一次性单个库下载):", self)
        self.newLine = QLineEdit(self)
        self.startAddButton = QPushButton("下载", self)
        self.closeAddButton = QPushButton("关闭", self)
        self.all_v_layout.addWidget(self.newName)
        self.tmpAdd_h_layout = QHBoxLayout()
        self.tmpAdd_h_layout.addWidget(self.newLine)
        self.tmpAdd_h_layout.addWidget(self.startAddButton)
        self.tmpAdd_h_layout.addWidget(self.closeAddButton)
        self.all_v_layout.addLayout(self.tmpAdd_h_layout)

        self.startAddButton.clicked.connect(self.startAddTmp)
        self.closeAddButton.clicked.connect(self.closeAddTmp)

    def startDelTmp(self):
        if self.delLine.text():
            deletePip = self.delLine.text().strip()
            res = subprocess.Popen("pip uninstall " + deletePip + " -y", shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, bufsize=-1)
            stderr = str(res.communicate()[1])
            if "as it is not installed." in stderr:
                QMessageBox.critical(self, "错误", "未找到库: " + deletePip, QMessageBox.Yes)
            else:
                QMessageBox.information(self, "操作成功", deletePip + " 卸载成功", QMessageBox.Yes)
            self.delLine.setText("")

    def closeDelTmp(self):
        self.pipFormStatus = 0
        self.delName.deleteLater()
        self.delLine.deleteLater()
        self.startDelButton.deleteLater()
        self.closeDelButton.deleteLater()

    def delPip(self):
        if self.pipFormStatus:
            return
        self.pipFormStatus = 1
        self.delName = QLabel("想要卸载的库名称(目前仅支持一次性单个库卸载):", self)
        self.delLine = QLineEdit(self)
        self.startDelButton = QPushButton("卸载", self)
        self.closeDelButton = QPushButton("关闭", self)
        self.all_v_layout.addWidget(self.delName)
        self.tmpDel_h_layout = QHBoxLayout()
        self.tmpDel_h_layout.addWidget(self.delLine)
        self.tmpDel_h_layout.addWidget(self.startDelButton)
        self.tmpDel_h_layout.addWidget(self.closeDelButton)
        self.all_v_layout.addLayout(self.tmpDel_h_layout)

        self.startDelButton.clicked.connect(self.startDelTmp)
        self.closeDelButton.clicked.connect(self.closeDelTmp)

    def startFindTmp(self):
        self.pipFormStatusFind = 1
        if self.findLine.text():
            findPip = self.findLine.text().strip()
            res = subprocess.Popen("pip show " + findPip, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   bufsize=-1)
            stdout = '\n'.join(str(res.communicate()[0])[2:-1].replace('\\r', '').split('\\n'))
            stderr = str(res.communicate()[1])
            if "Package(s) not found:" in stderr:
                QMessageBox.critical(self, "错误", "未找到库: " + findPip, QMessageBox.Yes)
            else:
                self.pipInfoLabel = QLabel("Pip库信息:", self)
                self.pipInfoText = QTextEdit(self)
                self.all_v_layout.addWidget(self.pipInfoLabel)
                self.all_v_layout.addWidget(self.pipInfoText)
                self.pipInfoText.setReadOnly(True)
                self.pipInfoText.setText(stdout)
                self.pipInfoText.setFont(QtGui.QFont("Microsoft YaHei", 11))
            self.findLine.setText("")

    def closeFindTmp(self):
        self.pipFormStatus = 0
        self.findName.deleteLater()
        self.findLine.deleteLater()
        self.startFindButton.deleteLater()
        self.closeFindButton.deleteLater()
        if self.pipFormStatusFind:
            self.pipInfoLabel.deleteLater()
            self.pipInfoText.deleteLater()
            self.pipFormStatusFind = 0

    def findPip(self):
        if self.pipFormStatus:
            return
        self.pipFormStatus = 1
        self.findName = QLabel("想要查找的库名称:", self)
        self.findLine = QLineEdit(self)
        self.startFindButton = QPushButton("查询", self)
        self.closeFindButton = QPushButton("关闭", self)
        self.all_v_layout.addWidget(self.findName)
        self.tmpFind_h_layout = QHBoxLayout()
        self.tmpFind_h_layout.addWidget(self.findLine)
        self.tmpFind_h_layout.addWidget(self.startFindButton)
        self.tmpFind_h_layout.addWidget(self.closeFindButton)
        self.all_v_layout.addLayout(self.tmpFind_h_layout)

        self.startFindButton.clicked.connect(self.startFindTmp)
        self.closeFindButton.clicked.connect(self.closeFindTmp)

    def listInit(self):
        self.pipList.setColumnCount(3)
        self.pipList.setHorizontalHeaderLabels(self.headers)
        self.pipList.setColumnWidth(0, 60)
        self.pipList.setColumnWidth(1, 420)
        self.pipList.setColumnWidth(2, 180)
        self.pipList.setShowGrid(False)
        self.pipList.verticalHeader().setHidden(True)
        self.pipList.setSelectionMode(QAbstractItemView.NoSelection)
        self.refreshList()
        self.pipList.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.pipList.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def findList(self):
        if self.pipList.itemClicked:
            print(1)

    def refreshList(self):
        self.clearRow()
        pipDict.clear()
        res = subprocess.Popen("pip list", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               bufsize=-1)
        info = res.communicate()
        pipLibs = [i.split() for i in str(info[0]).replace('\\r', '').split('\\n')[2:]][:-1]
        for i in range(len(pipLibs)):
            self.addRow(str(i), pipLibs[i][0], pipLibs[i][1])
            pipDict.update({i: pipLibs[i][0]})

    def show_aboutPage(self):
        self.about_page.exec_()

    def buttonInit(self):
        self.addButton.clicked.connect(self.addPip)
        self.delButton.clicked.connect(self.delPip)
        self.findButton.clicked.connect(self.findPip)
        self.refreshButton.clicked.connect(self.refreshList)
        self.aboutButton.clicked.connect(self.show_aboutPage)


class AboutPage(QDialog):
    def __init__(self):
        super(AboutPage, self).__init__()
        self.setWindowTitle("PIP库管理器 关于")
        self.resize(510, 200)
        self.authorLabel = QLabel("作者:", self)
        self.qqLabel = QLabel("QQ:", self)
        self.mailLabel = QLabel("邮箱:", self)
        self.githubLabel = QLabel("Github:", self)
        self.giteeLabel = QLabel("码云:", self)
        self.authorLine = QLineEdit(self)
        self.qqLine = QLineEdit(self)
        self.mailLine = QLineEdit(self)
        self.githubLine = QLineEdit(self)
        self.giteeLine = QLineEdit(self)
        self.githubButton = QPushButton("访问Github仓库", self)
        self.giteeButton = QPushButton("访问Gitee仓库", self)

        self.label_v_layout = QVBoxLayout()
        self.line_v_layout = QVBoxLayout()
        self.all_h_layout = QHBoxLayout()

        self.label_v_layout.addWidget(self.authorLabel)
        self.label_v_layout.addWidget(self.mailLabel)
        self.label_v_layout.addWidget(self.qqLabel)
        self.label_v_layout.addWidget(self.githubLabel)
        self.label_v_layout.addWidget(self.giteeLabel)
        self.label_v_layout.addWidget(self.githubButton)
        self.line_v_layout.addWidget(self.authorLine)
        self.line_v_layout.addWidget(self.mailLine)
        self.line_v_layout.addWidget(self.qqLine)
        self.line_v_layout.addWidget(self.githubLine)
        self.line_v_layout.addWidget(self.giteeLine)
        self.line_v_layout.addWidget(self.giteeButton)
        self.all_h_layout.addLayout(self.label_v_layout)
        self.all_h_layout.addLayout(self.line_v_layout)

        self.lineInit()
        self.buttonInit()
        self.setLayout(self.all_h_layout)

    def lineInit(self):
        self.authorLine.setReadOnly(True)
        self.mailLine.setReadOnly(True)
        self.qqLine.setReadOnly(True)
        self.githubLine.setReadOnly(True)
        self.giteeLine.setReadOnly(True)

        self.authorLine.setText("AuroraZ")
        self.mailLine.setText("2935876049@qq.com")
        self.qqLine.setText("2935876049")
        self.githubLine.setText("https://github.com/AuroraZiling/pipManager")
        self.giteeLine.setText("https://gitee.com/auroraziling/pipManager")

    def toGithub(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://github.com/AuroraZiling/pipManager'))

    def toGitee(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://gitee.com/auroraziling/pipManager'))

    def buttonInit(self):
        self.githubButton.clicked.connect(self.toGithub)
        self.giteeButton.clicked.connect(self.toGitee)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainForm()
    demo.show()
    sys.exit(app.exec_())
