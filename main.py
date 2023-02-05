import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPixmap

from design2 import Ui_MainWindow
from controller import Function

class Qui(QtWidgets.QMainWindow):
    """Класс интерфейса"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.obj_fun = Function() #экземпляр класса контроллера
        self.ui.pushButton_2.clicked.connect(self.finder)
        self.ui.pushButton_3.clicked.connect(self.graphic_zp)
        self.ui.pushButton_4.clicked.connect(self.graphic_requirement)
        self.ui.pushButton_6.clicked.connect(self.save)

        self.ui.tableWidget.horizontalScrollBar().setStyleSheet("""QScrollBar:horizontal{
                                                                    background-color: #060212; 
                                                                    border: 0px;
                                                                     }
                                                                    QScrollBar::handle:horizontal{
                                                                        background-color: #46405e;  }
                                                                        """)
        self.ui.tableWidget.verticalScrollBar().setStyleSheet("""QScrollBar:vertical{
                                                                    background-color: #060212; 
                                                                    border: 0px;
                                                                     }
                                                                 QScrollBar::handle:vertical{
                                                                    background-color: #46405e;  }""")
        self.ui.tableWidget.horizontalHeader().setDefaultSectionSize(135)
        self.ui.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{background: #060212; color: #5e6aa6; padding-left: 5px; padding-right: 5px; }")
        self.ui.tableWidget.verticalHeader().setStyleSheet("QHeaderView::section{background: #060212; color: #5e6aa6 }")
        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.setRowCount(2000)
        self.ui.tableWidget.setHorizontalHeaderLabels(["Название вакансии", "Ссылка", "Город" ,"Время публикации", "Зарплата от", "Зарплата до"])
    

    def finder(self):
        name_vac = self.ui.lineEdit.text()
        name_area = self.ui.lineEdit_2.text()
        self.mas_vacancies, self.mas_req = self.obj_fun.get_vac(name_vac, name_area)
        self.show_vac(self.mas_vacancies)


    def graphic_zp(self):
        self.obj_fun.graph_zp()
    

    def graphic_requirement(self):
        self.obj_fun.graph_names(self.mas_req)
    

    def save(self):
        self.obj_fun.save(self.mas_vacancies)


    def show_vac(self, mas_vac):
        # заполнение таблицы
        self.ui.tableWidget.setColumnCount(6)
        self.ui.tableWidget.setRowCount(len(mas_vac))
        self.ui.tableWidget.setHorizontalHeaderLabels(["Название вакансии", "Ссылка", "Город" ,"Время публикации", "Зарплата от", "Зарплата до"])
        
        for row in range(len(mas_vac)):
            for column in range(6):
                self.ui.tableWidget.setItem(row, column, QTableWidgetItem(mas_vac[row][column]))
        
        # отображение количества вакансий
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.appendPlainText(str(len(mas_vac)))

        # отображение вилки з/п
        mid, min, max = self.obj_fun.show_zp(mas_vac)
        self.ui.plainTextEdit_4.appendPlainText(mid) 
        self.ui.plainTextEdit_3.appendPlainText(min) 
        self.ui.plainTextEdit_5.appendPlainText(max)
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Qui()
    win.show()
    sys.exit(app.exec_())