import json, requests,time
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QInputDialog

from PyQt5.QtCore import QThread, QObject

from PyQt5 import QtCore, QtGui, QtWidgets

Form, Window = uic.loadUiType("style.ui")
broj_redova = 0
def dodaj_red_svojstva(s1, s2):
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

def obidji_listu_recnika(data, breadCrumbs):
	for i in range(0, len(data)):
		v = data[i]
		if type(v) in [bool, int, float] or v is None:
			v = str(v)
		if type(v) is str:
				dodaj_red_svojstva(breadCrumbs + " [" + str(i) + "] ", v)
		elif type(v) is dict:
				obidji_recnik(v, breadCrumbs + " [" + str(i) + "] ")
		if type(v) is list:
				obidji_listu_recnika(v, breadCrumbs + " [" + str(i) + "] ")


def obidji_recnik(data, breadCrumbs):
	for k,v in data.items():
		if type(v) in [bool, int, float] or v is None:
			v = str(v)
		if type(v) is str:
			if breadCrumbs == "":
				dodaj_red_svojstva(k, v)
			else:
				dodaj_red_svojstva(breadCrumbs + " > " + k, v)
		elif type(v) is dict:
			if breadCrumbs == "":
				obidji_recnik(v, k)
			else:
				obidji_recnik(v, breadCrumbs + " > " + k)
		if type(v) is list:
			if breadCrumbs == "":
				obidji_listu_recnika(v, k)
			else:
				obidji_listu_recnika(v, breadCrumbs + " > " + k)

def ucitaj_fajl():
	#text, ok = QInputDialog.getText(None, 'Input Dialog', 'Enter json of API:')
	#if not ok:
	#	return
	t0 = time.time()
	client_auth = requests.auth.HTTPBasicAuth('DEvmSWfEacPSTw', 'rdWGt_NxDFXEElLNrxCN3_no8z4')
	post_data = {"grant_type": "password", "username": "xyreason", "password": "mandat123"}
	headers = {"User-Agent": "QTreddit/0.1 by xyreason"}
	response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
	data = response.json()
	response.raise_for_status()
	headers = {"Authorization": "bearer "+ data[u"access_token"], "User-Agent": "QTreddit/0.1 by xyreason"}
	response = requests.get("https://oauth.reddit.com/.json?count=1", headers=headers)
	data = response.json()
	#print(json.dumps(data, sort_keys=True, indent=4))

	obidji_recnik(data, "")
	print(time.time() - t0)
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
form.pushButton.clicked.connect(dodaj_red)
form.pushButton_2.clicked.connect(obrisi_redove)
form.toolButton.clicked.connect(ucitaj_fajl)

window.show()
app.exec_()

