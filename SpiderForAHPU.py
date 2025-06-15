import sys

from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QApplication
from qfluentwidgets import (NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF
from PySide6.QtCore import Qt, QUrl
from Views.QueryScoresView import QueryScoresView


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))



class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # 创建子页面
        self.homeInterface = Widget('Home Interface', self)
        self.queryCourseView = Widget('课表', self)
        self.queryExamView = Widget('考试', self)
        self.queryScoreView = QueryScoresView()

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.queryCourseView, FIF.EDUCATION, '课表')
        self.addSubInterface(self.queryExamView, FIF.PENCIL_INK, '考试')
        self.addSubInterface(self.queryScoreView, FIF.BOOK_SHELF, '成绩')

        # 添加自定义导航组件
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(1280, 700)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('安徽工程大学教务系统')

    def showMessageBox(self):
        w = MessageBox(
            '支持作者🥰',
            '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀',
            self
        )
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://qfluentwidgets.com/zh/price/"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
