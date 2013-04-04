from PySide import QtCore, QtGui


class MyDate(QtCore.QDate):
    
    def __init__(self, date):
        super(MyDate, self).__init__()
        self.setDate(date.year(), date.month(), date.day())
        
    def toStringHeader(self):
        return '{3:s} {0:02d}.{1:02d}.{2:d}'.format(
            self.day(), self.month(), self.year(), 
            QtCore.QDate.shortDayName(self.dayOfWeek()))


class WdwCalendar(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(WdwCalendar, self).__init__(parent=parent)
        self.loCalendar = QtGui.QVBoxLayout()
        self.calendar = QtGui.QCalendarWidget(parent=self)
        self.calendar.setFirstDayOfWeek(1)
        parent.dateCurrent = self.calendar.selectedDate()
        self.buttonOpenWeek = QtGui.QPushButton('Open Week', parent=self)
        self.buttonOpenWeek.clicked.connect(parent.openWeek)
        self.calendar.clicked.connect(self.setCurrentDate)
        self.loCalendar.addWidget(self.calendar)
        self.loCalendar.addWidget(self.buttonOpenWeek)      
        self.setLayout(self.loCalendar)
        
    def setCurrentDate(self, date):
        parent = self.parent()
        parent.dateCurrent = date

        
        
class WdwWeek(QtGui.QWidget):
    
    def __init__(self, model, parent=None):
        super(WdwWeek, self).__init__(parent=parent)
        self.model = model
        self.loWeek = QtGui.QVBoxLayout()
        self.tableView = QtGui.QTableView(parent=self)      
        self.tableView.setModel(self.model)
        self.tableView.setDragEnabled(True)
        dragMode = QtGui.QAbstractItemView.DragDropMode(2)
        self.tableView.setDragDropMode(dragMode)
        self.buttonSaveWeek = QtGui.QPushButton('Save Week', parent=self)
        self.buttonSaveWeek.clicked.connect(parent.openCalendar)   
        self.loWeek.addWidget(self.tableView)
        self.loWeek.addWidget(self.buttonSaveWeek)        
        self.setLayout(self.loWeek)
        for i in parent.daysInWeek:
            self.tableView.setColumnWidth(i, parent.columnWidth)
        
    def test(self, x):
        print(x)
            
            
class WdwLogin(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(WdwLogin, self).__init__(parent=parent)
        self.loLogin = QtGui.QVBoxLayout()
        self.loLogin.setAlignment(QtCore.Qt.AlignTop)
        self.textLogin = QtGui.QLineEdit(parent=self)
        self.textPassword = QtGui.QLineEdit(parent=self)
        self.textPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton('Login', parent=self)
        self.buttonLogin.clicked.connect(self.login)
        self.loLogin.addWidget(self.textLogin)
        self.loLogin.addWidget(self.textPassword)
        self.loLogin.addWidget(self.buttonLogin)
        self.setLayout(self.loLogin)
        
    def login(self):
        self.parent().user = self.textLogin.text()
        self.parent().initCalendar()
        

class MainApplication(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainApplication, self).__init__(parent=None)
        self.windowSize = (100, 100, 700, 500) 
        self.daysInWeek = range(7)
        self.hoursInDay = range(0, 24)
        self.columnWidth = 200
        self.model = QtGui.QStandardItemModel(
            len(self.hoursInDay), len(self.daysInWeek))
        self.initUI()
        self.setGeometry(*self.windowSize)
        
    def initUI(self):
        self.menu = self.menuBar()
        self.menuFile = self.menu.addMenu('&File')
        self.saveAction = QtGui.QAction('&Save', self)
        self.saveAction.triggered.connect(self.saveAll)
        self.menuFile.addAction(self.saveAction)
        self.status = self.statusBar()
        self.initLogin()
        
    def initLogin(self):
        self.wdwLogin = WdwLogin(parent=self)
        self.setCentralWidget(self.wdwLogin)
        
    def initCalendar(self):
        self.wdwCalendar = WdwCalendar(parent=self)
        self.setCentralWidget(self.wdwCalendar)
        
    def initWeek(self):
        self.wdwWeek = WdwWeek(self.model, parent=self)
        
    def openCalendar(self):
        self.initCalendar()
        self.setCentralWidget(self.wdwCalendar)
        
    def openWeek(self):
        self.initWeek()
        self.updateWeekHeader()
        self.setCentralWidget(self.wdwWeek)
        
    def updateWeekHeader(self):
        date = self.dateCurrent.addDays(1 - self.dateCurrent.dayOfWeek())
        days = [MyDate(date.addDays(i)).toStringHeader() 
            for i in self.daysInWeek]
        hours = ['{0:02d}:00'.format(i) for i in self.hoursInDay]
        self.model.setHorizontalHeaderLabels(days)
        self.model.setVerticalHeaderLabels(hours)
        
    def saveAll(self):
        self.status.showMessage('saved')


if __name__ == '__main__':
    app = QtGui.QApplication([])
    ma = MainApplication()
    ma.show()
    app.exec_()