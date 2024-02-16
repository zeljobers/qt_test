import json, requests, sys, time, threading
from tqdm import tqdm
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QInputDialog

from PyQt5.QtCore import QThread, QObject

from PyQt5 import QtCore, QtGui, QtWidgets

Form, Window = uic.loadUiType("style.ui")
broj_redova = 0

def dodaj_red_svojstva(s1, s2, sig):
	#print(s1, s2)
	global form, broj_redova
	broj_redova += 1
	horizontalLayout_3 = QtWidgets.QHBoxLayout()
	horizontalLayout_3.setObjectName("horizontalLayout_3")
	label = QtWidgets.QLabel(form.centralwidget)
	sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
	sizePolicy.setHorizontalStretch(0)
	sizePolicy.setVerticalStretch(12)
	sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
	label.setSizePolicy(sizePolicy)
	label.setText(str(s1))
	label.setObjectName("label")
	horizontalLayout_3.addWidget(label)
	textEdit = QtWidgets.QTextEdit(form.centralwidget)
	sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
	sizePolicy.setHorizontalStretch(0)
	sizePolicy.setVerticalStretch(12)
	sizePolicy.setHeightForWidth(textEdit.sizePolicy().hasHeightForWidth())
	textEdit.setText(str(s2))
	textEdit.setSizePolicy(sizePolicy)
	textEdit.setObjectName("textEdit")
	textEdit.setSizePolicy(sizePolicy)
	textEdit.setMinimumSize(QtCore.QSize(0, 12))
	textEdit.setMaximumSize(QtCore.QSize(16777215, 24))
	textEdit.setBaseSize(QtCore.QSize(0, 12))
	textEdit.setObjectName("textEdit")
	horizontalLayout_3.addWidget(textEdit)
	form.verticalLayout_2.addLayout(horizontalLayout_3)
	sig.set()


def dodaj_red():
	global form, broj_redova
	broj_redova += 1
	horizontalLayout_3 = QtWidgets.QHBoxLayout()
	horizontalLayout_3.setObjectName("horizontalLayout_3")
	label = QtWidgets.QLabel(form.centralwidget)
	sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
	sizePolicy.setHorizontalStretch(0)
	sizePolicy.setVerticalStretch(12)
	sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
	label.setSizePolicy(sizePolicy)
	label.setText("Red broj" + str(broj_redova))
	label.setObjectName("label")
	horizontalLayout_3.addWidget(label)
	textEdit = QtWidgets.QTextEdit(form.centralwidget)
	sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
	sizePolicy.setHorizontalStretch(0)
	sizePolicy.setVerticalStretch(12)
	sizePolicy.setHeightForWidth(textEdit.sizePolicy().hasHeightForWidth())
	textEdit.setSizePolicy(sizePolicy)
	textEdit.setObjectName("textEdit")
	textEdit.setSizePolicy(sizePolicy)
	textEdit.setMinimumSize(QtCore.QSize(0, 12))
	textEdit.setMaximumSize(QtCore.QSize(16777215, 24))
	textEdit.setBaseSize(QtCore.QSize(0, 12))
	textEdit.setObjectName("textEdit")
	horizontalLayout_3.addWidget(textEdit)
	form.verticalLayout_2.addLayout(horizontalLayout_3)

def obrisi_redove_rek(layout):
	while layout.count():
		child = layout.takeAt(0)
		if child.widget() is not None:
			child.widget().deleteLater()
		elif child.layout() is not None:
			obrisi_redove_rek(child.layout())

def obrisi_redove():
	global form, broj_redova
	broj_redova= 0
	layout = form.verticalLayout_2
	obrisi_redove_rek(layout)
class Obilazak:
	def __init__(self):
		self.worker = _Obilazak()

class _Obilazak(QThread):
	gotovo = QtCore.pyqtSignal(str, str, threading.Event)
	
	def __init__(self, parent=None):
		QThread.__init__(self, parent)

	def run(self):
		
		t0 = time.time()
		client_auth = requests.auth.HTTPBasicAuth('DEvmSWfEacPSTw', 'rdWGt_NxDFXEElLNrxCN3_no8z4')
		post_data = {"grant_type": "password", "username": "xyreason", "password": "mandat123"}
		headers = {"User-Agent": "QTreddit/0.1 by xyreason"}
		response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
		data = response.json()
		response.raise_for_status()
		headers = {"Authorization": "bearer "+ data[u"access_token"], "User-Agent": "QTreddit/0.1 by xyreason"}
		response = requests.get("https://oauth.reddit.com/.json?count=10", headers=headers)
		self.data = response.json()
		self.breadCrumbs = ''
		#print(json.dumps(data, sort_keys=True, indent=4))
		
		self.obidji_recnik(self.data, self.breadCrumbs)
		print(time.time() - t0)

	def obidji_listu_recnika(self, data, breadCrumbs):
		for i in range(0, len(data)):
			v = data[i]
			if type(v) in [bool, int, float] or v is None:
				v = str(v)
			if type(v) is str:
					e = threading.Event()
					self.gotovo.emit(breadCrumbs + " [" + str(i) + "] ", v, e)
					#time.sleep(0.1) # nije nuzno
					e.wait()
					
			elif type(v) is dict:
					self.obidji_recnik(v, breadCrumbs + " [" + str(i) + "] ")
			if type(v) is list:
					self.obidji_listu_recnika(v, breadCrumbs + " [" + str(i) + "] ")

	def obidji_recnik(self, data, breadCrumbs):
		for k,v in data.items():
			if type(v) in [bool, int, float] or v is None:
				v = str(v)
			if type(v) is str:
				if breadCrumbs == "":
					e = threading.Event()
					self.gotovo.emit(k, v, e)
					#time.sleep(0.1) # nije nuzno
					e.wait()
				else:
					e = threading.Event()
					self.gotovo.emit(breadCrumbs + " > " + k, v, e)
					# time.sleep(0.1) # glavno za brzinu, glatkost guia
					# al jebi ga opet ce da koci
					e.wait()

			elif type(v) is dict:
				if breadCrumbs == "":
					self.obidji_recnik(v, k)
				else:

					self.obidji_recnik(v, breadCrumbs + " > " + k)
			if type(v) is list:
				if breadCrumbs == "":
					self.obidji_listu_recnika(v, k)
				else:
					self.obidji_listu_recnika(v, breadCrumbs + " > " + k)
				
def obidji_recnik():
	global neki_qthread # ovo sprecava QThread : Destroyed 
	neki_qthread = Obilazak() 
	# na window-a ce da ceka, inace izlazi QThread: Destroyed while thread is still running 
	# a onda izadje jos gora greska nego prosla
	# onda metnes klasu wrapper, a ono jos gore radi nego pre
	# resio sam to: tako sto sam prestao da pravim u rekurzivnim koracima tredove
	neki_qthread.worker.gotovo.connect( dodaj_red_svojstva)
	neki_qthread.worker.start()
	

def ucitaj_fajl():
	#text, ok = QInputDialog.getText(None, 'Input Dialog', 'Enter json of API:')
	#if not ok:
	#	return
	obidji_recnik()
def dodaj_red_1():
	for i in range(0, 1000):
		dodaj_red()		
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.pushButton.clicked.connect(dodaj_red_1)
form.pushButton_2.clicked.connect(obrisi_redove)
form.toolButton.clicked.connect(ucitaj_fajl)

window.show()
sys.exit(app.exec_())

