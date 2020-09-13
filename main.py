"""
Emirhan Yılmaz
10.09.2020
"""
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image
from PyQt5.QtWidgets import QMessageBox

con = sqlite3.connect("emp.db")
cur = con.cursor()
defaultImage = "person.png"
person_id = None
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Employees")
        self.setGeometry(350, 150, 650, 500)
        self.UI()
        self.show()

    def UI(self):
        self.mainDesign()
        self.layouts()
        self.getEmp()
        if self.employeelist.count() > 0:
            self.displayFirst()
    def layouts(self):
        # #########LAYOUTLAR################
        self.mainlayout = QHBoxLayout()
        self.form = QFormLayout()
        self.rightbox = QVBoxLayout()
        self.list = QHBoxLayout()
        self.hbox = QHBoxLayout()
        # adding child layouts to main layout
        self.rightbox.addLayout(self.list)
        self.rightbox.addLayout(self.hbox)
        self.mainlayout.addLayout(self.form,40)
        self.mainlayout.addLayout(self.rightbox,60)
        # #adding widgets to layouts
        self.list.addWidget(self.employeelist)
        self.hbox.addWidget(self.btnNew)
        self.hbox.addWidget(self.btnUpdate)
        self.hbox.addWidget(self.btnDel)

        # setting main window layout
        self.setLayout(self.mainlayout)
    def mainDesign(self):
        self.setStyleSheet("font-size:13pt;font-family:Ariel;")
        self.employeelist = QListWidget()
        self.employeelist.itemClicked.connect(self.showPerson)
        self.btnNew = QPushButton("New")
        self.btnNew.clicked.connect(self.addEmp)
        self.btnUpdate = QPushButton("Update")
        self.btnUpdate.clicked.connect(self.updateEmp)
        self.btnDel = QPushButton("Delete")
        self.btnDel.clicked.connect(self.deleteEmp)

    def updateEmp(self):
        global person_id
        if self.employeelist.selectedItems():
            person = self.employeelist.currentItem().text()
            person_id = person.split("-")[0]
            self.updateWindow = UpdateWindow()
            self.close()
    def deleteEmp(self):
        if self.employeelist.selectedItems():
            person = self.employeelist.currentItem().text()
            id = person.split("-")[0]
            mbox = QMessageBox.question(self, "Warning!", "Are you sure to delete this person", QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query = "DELETE FROM emp WHERE id=?"
                    cur.execute(query, (id,))
                    con.commit()
                    QMessageBox.information(self, "Info!", "Person has been deleted")
                    self.close()
                    self.main = Main()
                except:
                    QMessageBox.information(self, "Warning!", "Person has not be deleted")

    def showPerson(self):
        for i in reversed(range(self.form.count())):
            widget = self.form.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.displayFirst()

    def addEmp(self):
        self.newEmp = AddEmployee()
        self.close()
    def getEmp(self):
        query = "SELECT id,name,surname FROM emp"
        employees = cur.execute(query).fetchall()
        for employee in employees:
            self.employeelist.addItem(str(employee[0])+"-"+employee[1]+" "+employee[2])
    def displayFirst(self):
        try:
            employee = self.employeelist.currentItem().text()
            id = employee.split("-")[0]
            query = "SELECT * FROM emp WHERE id=?"
            employee = cur.execute(query, (id,)).fetchone()
        except:
            query = "SELECT * FROM emp ORDER BY ROWID ASC LIMIT 1"
            employee = cur.execute(query).fetchone()

        img = QLabel()
        img.setPixmap(QPixmap("images/"+employee[5]))
        self.form.setVerticalSpacing(20)
        self.form.addRow("", img)
        self.form.setAlignment(Qt.AlignCenter)
        self.form.addRow("Name :", QLabel(employee[1]))
        self.form.addRow("Surname :", QLabel(employee[2]))
        self.form.addRow("Phone :", QLabel(employee[3]))
        self.form.addRow("Email :", QLabel(employee[4]))
        self.form.addRow("Adress :", QLabel(employee[6]))

class UpdateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Employee")
        self.setStyleSheet("background-color:white")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()

    def UI(self):
        self.getPerson()
        self.mainDesign()
        self.layouts()
    def closeEvent(self, event):
        self.main = Main()

    def getPerson(self):
        global person_id
        query = "SELECT * FROM emp WHERE id=?"
        employee = cur.execute(query,(person_id,)).fetchone()
        self.namee = employee[1]
        self.surnamee = employee[2]
        self.phonee = employee[3]
        self.emaill = employee[4]
        self.imgg = employee[5]
        self.adres = employee[6]
    def layouts(self):
        # main layouts
        self.main = QVBoxLayout()
        self.top = QVBoxLayout()
        self.bottom = QFormLayout()
        # adding child layouts
        self.main.addLayout(self.top)
        self.main.addLayout(self.bottom)
        # adding top layout widgets
        self.top.addWidget(self.title)
        self.top.addWidget(self.img)
        self.top.addStretch()
        self.top.setAlignment(Qt.AlignCenter)
        # adding bottom layout widgets
        self.bottom.addRow(self.name, self.nameEntry)
        self.bottom.addRow(self.surname, self.surnameEntry)
        self.bottom.addRow(self.phone, self.phoneEntry)
        self.bottom.addRow(self.email, self.emailEntry)
        self.bottom.addRow(self.imglbl, self.imgbtn)
        self.bottom.addRow(self.adreslbl, self.adressEditor)
        self.bottom.addRow("", self.upbtn)
        # setting main layout for window
        self.setLayout(self.main)

    def mainDesign(self):
        # Top layout widgets
        self.title = QLabel("Update Person")
        self.title.setStyleSheet('font-size:24pt;font-family:Arial Bold')
        self.img = QLabel()
        self.img.setPixmap(QPixmap("images/{}".format(self.imgg)))
        # bottom layout widgets
        self.name = QLabel("Name :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.namee)
        self.surname = QLabel("Surname :")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setText(self.surnamee)
        self.phone = QLabel("Phone :")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.phonee)
        self.email = QLabel("Email :")
        self.emailEntry = QLineEdit()
        self.emailEntry.setText(self.emaill)
        self.imglbl = QLabel("Picture :")
        self.imgbtn = QPushButton("Browse")
        self.imgbtn.setStyleSheet("background-color:orange;font-size:10pt")
        self.imgbtn.clicked.connect(self.uploadim)
        self.adreslbl = QLabel("Adress :")
        self.adressEditor = QTextEdit()
        self.adressEditor.setText(self.adres)
        self.upbtn = QPushButton("Update")
        self.upbtn.setStyleSheet("background-color:orange;font-size:10pt")
        self.upbtn.clicked.connect(self.updatePer)

    def updatePer(self):
        global defaultImage
        global person_id
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        img = defaultImage
        address = self.adressEditor.toPlainText()
        if (name and surname and phone != ""):
            try:
                query = "UPDATE emp set name=?,surname=?,phone=?,email=?,img=?,adress=? WHERE id=?"
                cur.execute(query, (name, surname, phone, email, img, address, person_id))
                con.commit()
                QMessageBox.information(self, "Success!", "Person has been updated")
                self.close()
                self.main = Main()
            except:
                QMessageBox.information(self, "Warning!", "Person has not been updated")
        else:
            QMessageBox.information(self, "Warning", "Fields can'nt ne empty")

    def uploadim(self):
        global defaultImage
        size = (128, 128)
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Upload Image", '', 'Image Files (*.jpg *.png)' )
        print(self.fileName)
        if ok:
            defaultImage = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(defaultImage))
            self.img.setPixmap(QPixmap("images/{}".format(defaultImage)))

class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Employee")
        self.setStyleSheet("background-color:white")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()
    def closeEvent(self, event):
        self.main = Main()
    def UI(self):
        self.mainDesign()
        self.layouts()
    def layouts(self):
        # main layouts
        self.main = QVBoxLayout()
        self.top = QVBoxLayout()
        self.bottom = QFormLayout()
        # adding child layouts
        self.main.addLayout(self.top)
        self.main.addLayout(self.bottom)
        # adding top layout widgets
        self.top.addWidget(self.title)
        self.top.addWidget(self.img)
        self.top.addStretch()
        self.top.setAlignment(Qt.AlignCenter)
        # adding bottom layout widgets
        self.bottom.addRow(self.name, self.nameEntry)
        self.bottom.addRow(self.surname, self.surnameEntry)
        self.bottom.addRow(self.phone, self.phoneEntry)
        self.bottom.addRow(self.email, self.emailEntry)
        self.bottom.addRow(self.imglbl, self.imgbtn)
        self.bottom.addRow(self.adreslbl, self.adressEditor)
        self.bottom.addRow("", self.addbtn)
        # setting main layout for window
        self.setLayout(self.main)
    def mainDesign(self):
        # Top layout widgets
        self.title = QLabel("Add Person")
        self.title.setStyleSheet('font-size:24pt;font-family:Arial Bold')
        self.img = QLabel()
        self.img.setPixmap(QPixmap("icons\person.png"))
        # bottom layout widgets
        self.name = QLabel("Name :")
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Employee Name")
        self.surname = QLabel("Surname :")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter Employee Surname")
        self.phone = QLabel("Phone :")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter Employee Phone Number")
        self.email = QLabel("Email :")
        self.emailEntry = QLineEdit()
        self.emailEntry.setPlaceholderText("Enter Employee Email Adress")
        self.imglbl = QLabel("Picture :")
        self.imgbtn = QPushButton("Browse")
        self.imgbtn.clicked.connect(self.uploadim)
        self.imgbtn.setStyleSheet("background-color:orange;font-size:10pt")
        self.adreslbl = QLabel("Adress :")
        self.adressEditor = QTextEdit()
        self.addbtn = QPushButton("Add")
        self.addbtn.clicked.connect(self.addEmp)
        self.addbtn.setStyleSheet("background-color:orange;font-size:10pt")
        self.adreslbl = QLabel("Adress :")
    def addEmp(self):
        global defaultImage
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        img = defaultImage
        adress = self.adressEditor.toPlainText()
        if (name and surname and phone != ""):
            try:
                query = "INSERT INTO emp (name,surname,phone,email,img,adress) VALUES(?,?,?,?,?,?)"
                cur.execute(query, (name,surname,phone,email,img,adress))
                con.commit()
                QMessageBox.information(self, "Success!", "Person has been added")
                self.close()
                self.main = Main()
            except:
                QMessageBox.information(self, "Warning!", "Person has not been added")
        else:
            QMessageBox.information(self, "Warning", "Fields can'nt ne empty")

    def uploadim(self):
        global defaultImage
        size = (128, 128)
        self.fileName, ok = QFileDialog.getOpenFileName(self, "Upload Image", '', 'Image Files (*.jpg *.png)' )
        print(self.fileName)
        if ok:
            defaultImage = os.path.basename(self.fileName)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save("images/{}".format(defaultImage))
            self.img.setPixmap(QPixmap("images/{}".format(defaultImage)))
def main():
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()