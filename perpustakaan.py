from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
    QAbstractItemView
)
import sys

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 420)

        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(150, 15, 220, 25))

        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        self.label.setFont(font)

        # Input Judul Buku
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(80, 60, 80, 20))

        self.txtJudul = QtWidgets.QLineEdit(parent=Form)
        self.txtJudul.setGeometry(QtCore.QRect(180, 60, 180, 25))
        self.txtJudul.setStyleSheet(
            "background-color: rgb(255, 98, 242);"
        )

        # Input Penulis
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(80, 95, 80, 20))

        self.txtPenulis = QtWidgets.QLineEdit(parent=Form)
        self.txtPenulis.setGeometry(QtCore.QRect(180, 95, 180, 25))
        self.txtPenulis.setStyleSheet(
            "background-color: rgb(255, 98, 242);"
        )

        # Input Tahun
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(80, 130, 100, 20))

        self.txtTahun = QtWidgets.QLineEdit(parent=Form)
        self.txtTahun.setGeometry(QtCore.QRect(180, 130, 180, 25))
        self.txtTahun.setStyleSheet(
            "background-color: rgb(255, 98, 242);"
        )

        # Tombol Tambah
        self.btnTambah = QtWidgets.QPushButton(parent=Form)
        self.btnTambah.setGeometry(QtCore.QRect(150, 180, 90, 30))
        self.btnTambah.setStyleSheet(
            "background-color: rgb(234, 111, 255);"
        )

        # Tombol Hapus
        self.btnHapus = QtWidgets.QPushButton(parent=Form)
        self.btnHapus.setGeometry(QtCore.QRect(260, 180, 90, 30))
        self.btnHapus.setStyleSheet(
            "background-color: rgb(234, 111, 255);"
        )

        # Tabel
        self.tableBuku = QtWidgets.QTableWidget(parent=Form)
        self.tableBuku.setGeometry(QtCore.QRect(40, 240, 420, 150))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate

        Form.setWindowTitle(
            _translate("Form", "Aplikasi Perpustakaan")
        )

        self.label.setText(
            _translate("Form", "APLIKASI PERPUSTAKAAN")
        )

        self.label_2.setText(
            _translate("Form", "Judul Buku")
        )

        self.label_3.setText(
            _translate("Form", "Penulis")
        )

        self.label_4.setText(
            _translate("Form", "Tahun Terbit")
        )

        self.btnTambah.setText(
            _translate("Form", "Tambah")
        )

        self.btnHapus.setText(
            _translate("Form", "Hapus")
        )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Aplikasi Perpustakaan")

        # Input tahun hanya angka
        self.ui.txtTahun.setValidator(
            QIntValidator(0, 9999)
        )

        # Pengaturan tabel
        self.ui.tableBuku.setColumnCount(3)
        self.ui.tableBuku.setHorizontalHeaderLabels(
            ["Judul Buku", "Penulis", "Tahun Terbit"]
        )

        self.ui.tableBuku.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.ui.tableBuku.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.ui.tableBuku.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.ui.btnTambah.clicked.connect(
            self.tambah_buku
        )

        self.ui.btnHapus.clicked.connect(
            self.hapus_buku
        )

        self.load_data()

    def tambah_buku(self):
        judul = self.ui.txtJudul.text().strip()
        penulis = self.ui.txtPenulis.text().strip()
        tahun = self.ui.txtTahun.text().strip()

        if not judul or not penulis or not tahun:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Semua data harus diisi!"
            )
            return

        row = self.ui.tableBuku.rowCount()
        self.ui.tableBuku.insertRow(row)

        self.ui.tableBuku.setItem(
            row, 0, QTableWidgetItem(judul)
        )

        self.ui.tableBuku.setItem(
            row, 1, QTableWidgetItem(penulis)
        )

        self.ui.tableBuku.setItem(
            row, 2, QTableWidgetItem(tahun)
        )

        self.simpan_data()

        self.ui.txtJudul.clear()
        self.ui.txtPenulis.clear()
        self.ui.txtTahun.clear()

        QMessageBox.information(
            self,
            "Berhasil",
            "Data buku berhasil ditambahkan."
        )

    def hapus_buku(self):
        row = self.ui.tableBuku.currentRow()

        if row == -1:
            QMessageBox.warning(
                self,
                "Peringatan",
                "Pilih data yang ingin dihapus!"
            )
            return

        jawab = QMessageBox.question(
            self,
            "Konfirmasi",
            "Yakin ingin menghapus data ini?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if jawab == QMessageBox.StandardButton.Yes:
            self.ui.tableBuku.removeRow(row)
            self.simpan_data()

    def load_data(self):
        try:
            with open(
                "data_buku.txt",
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:
                    data = line.strip().split(",")

                    if len(data) == 3:
                        row = self.ui.tableBuku.rowCount()
                        self.ui.tableBuku.insertRow(row)

                        self.ui.tableBuku.setItem(
                            row, 0,
                            QTableWidgetItem(data[0])
                        )

                        self.ui.tableBuku.setItem(
                            row, 1,
                            QTableWidgetItem(data[1])
                        )

                        self.ui.tableBuku.setItem(
                            row, 2,
                            QTableWidgetItem(data[2])
                        )

        except FileNotFoundError:
            pass

    def simpan_data(self):
        with open(
            "data_buku.txt",
            "w",
            encoding="utf-8"
        ) as file:

            for row in range(
                self.ui.tableBuku.rowCount()
            ):
                judul = self.ui.tableBuku.item(
                    row, 0
                ).text()

                penulis = self.ui.tableBuku.item(
                    row, 1
                ).text()

                tahun = self.ui.tableBuku.item(
                    row, 2
                ).text()

                file.write(
                    f"{judul},{penulis},{tahun}\n"
                )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())