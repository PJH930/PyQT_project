import sys
from distutils.dir_util import copy_tree
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy
import pandas as pd
from pandas import Series, DataFrame

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("GUI_project_9.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self):
        super().__init__()
        # setFixedSize : 윈도우 창 사이즈 고정하기
        # self.setFixedSize(QSize(780, 460))
        self.setupUi(self)

#   ----------------------------↓↓↓변수↓↓↓-----------------------------------

        # 실행 파일의 절대값을 저장 리스트
        self.open_list = []

        # 데이터셋 파일 저장 리스트
        self.dataset_list_dir = []

        # 데이터셋 적용폴더 저장 리스트
        self.dataset_dir = []

        # 결과폴더 절대경로
        self.result_dir =[]

        # 텍스트 데이터 모든파일의 절대경로
        self.text_all_list = []

        # 그림 데이터 모든파일의 절대경로
        self.img_all_list = []

        # 화면에 표시된 데이터셋 파일과 결과파일의 절대값 주소
        self.original_img = ""
        self.result_img_img = ""

        # treeView 목록 파일을 클릭하면 그 파일의 절대값을 저장해줌
        self.tree_View_file_click = ""

#   ----------------------------↑↑↑변수↑↑↑-----------------------------------

#   ----------------------------↓↓↓버튼↓↓↓-----------------------------------

        # 모델/데이터셋 불러오기 버튼
        self.pushButton_1.clicked.connect(self.modelSelect)
        self.pushButton_2.clicked.connect(self.datasetDirSelect)

        # open_list에 저장해둔 파일 실행 버튼
        self.pushButton_3.clicked.connect(self.runFile)

        # 데이터셋 복사 버튼
        self.pushButton_4.clicked.connect(self.datasetDir)

        # 결과폴더 선택버튼
        self.pushButton_7.clicked.connect(self.resultDir)

        # 결과확인 버튼 test
        # self.pushButton_result.clicked.connect(self.)

        # self.fig = plt.Figure()
        # self.canvas = FigureCanvas(self.fig)

#   ----------------------------↑↑↑버튼↑↑↑-----------------------------------

#   ----------------------------↓↓↓함수들↓↓↓-----------------------------------

    # 모델위치 선택 함수
    def modelSelect(self):
        file_path = QFileDialog.getOpenFileName(self, 'Attach File')[0]
        # self.textEdit_1.setText(file_path)
        self.open_list.append(file_path)
        # print('Selected model:', file_path)

    # 데이터셋이 들어있는 폴더를 선택하는 함수
    def datasetDirSelect(self):
        file_path = QFileDialog.getExistingDirectory(self, "select Directory")
        # self.textEdit_2.setText(file_path)
        self.dataset_list_dir.append(file_path)
        # print('Selected Dir:', file_path)
        self.model_file_system = QFileSystemModel()
        self.model_file_system.setRootPath(file_path)
        self.model_file_system.setReadOnly(False)
        self.treeView.setModel(self.model_file_system)
        self.treeView.setRootIndex(self.model_file_system.index(file_path))
        self.treeView.doubleClicked.connect(lambda index: self.treeViewDoubleClicked(index))
        self.treeView.setDragEnabled(True)
        self.treeView.setColumnWidth(0, 300)

    # treeView 더블클릭 시 절대값 추출함수
    def treeViewDoubleClicked(self, index):
        self.tree_View_file_click = self.model_file_system.filePath(index)
        self.original_img = self.tree_View_file_click
        pixmap = QPixmap(self.tree_View_file_click)
        pixmap = pixmap.scaled(self.label.size(), aspectRatioMode=True)
        self.label.setPixmap(pixmap)

    def treeViewDoubleClicked_2(self, index):
        self.tree_View_file_click = self.model_file_system.filePath(index)
        self.result_img = self.tree_View_file_click
        pixmap = QPixmap(self.tree_View_file_click)
        pixmap = pixmap.scaled(self.label_2.size(), aspectRatioMode=True)
        self.label_2.setPixmap(pixmap)

    # 실행버튼 함수
    def runFile(self):
        copy_tree(self.dataset_list_dir[0], self.dataset_dir[0])
        file_path = self.open_list[0]
        process = QProcess(self)
        process.start('python', [file_path])

    # 데이터셋을 적용할 폴더 선택 함수
    def datasetDir(self):
        directory_path = QFileDialog.getExistingDirectory(self, "select Directory")
        # self.textEdit_4.setText(directory_path)
        self.dataset_dir.append(directory_path)

    # 결과폴더 선택
    def resultDir(self):
        file_path = QFileDialog.getExistingDirectory(self, "select Directory")
        self.result_dir.append(file_path)
        # print('Selected Dir:', file_path)
        self.model_file_system = QFileSystemModel()
        self.model_file_system.setRootPath(file_path)
        self.model_file_system.setReadOnly(False)
        self.treeView_2.setModel(self.model_file_system)
        self.treeView_2.setRootIndex(self.model_file_system.index(file_path))
        self.treeView_2.doubleClicked.connect(lambda index: self.treeViewDoubleClicked_2(index))
        self.treeView_2.setDragEnabled(True)
        self.treeView_2.setColumnWidth(0, 300)

    # 차트로 표시해줄 함수
    def cartInfo(self):

        self.canvas.draw()

#   ----------------------------↑↑↑함수들↑↑↑-----------------------------------

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
