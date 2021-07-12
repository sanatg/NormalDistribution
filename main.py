# read the commands to run this project:
    # commands for linux:
    #     pip install PyQtWebEngine
    #     pip install PyQt5
    #     pip install pandas
    #     pip install plotly
    #     python3 main.py
    # commands for macosx:
    #     pip install PyQtWebEngine
    #     pip install PyQt5
    #     pip install pandas
    #     pip install plotly
    #     python3 main.py

import plotly.figure_factory as ff
import plotly.graph_objects as go
import csv
import statistics as stat
import pandas as pd
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import plotly.express as px

class Widget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Click me to plot the graph', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)
        vlayout.addWidget(self.browser)

        self.button.clicked.connect(self.show_graph)
        self.resize(1000,800)

    def show_graph(self):
        #plotting the chart, and lines for the mean,1st standard deviation,2nd standard deviations
        fig = ff.create_distplot([data], ['reading scores'], show_hist = False)
        fig.add_trace(go.Scatter(x=[mean,mean], y=[0,0.17], mode='lines', name='MEAN')),
        fig.add_trace(go.Scatter(x=[first_standard_deviation_start,first_standard_deviation_end], y=[0,0.17], mode='lines', name='1st STD')),
        fig.add_trace(go.Scatter(x=[second_standard_deviation_start,second_standard_deviation_end], y=[0,0.17], mode='lines', name='2nd STD')),
        fig.add_trace(go.Scatter(x=[third_standard_deviation_start,third_standard_deviation_end], y=[0,0.17], mode='lines', name='3rd STD')),
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))
        
#reading score data
score_data = pd.read_csv('score.csv')

#data for bar plot
data = score_data['reading score'].tolist()

#calculating the mean,median,mode and standard deviation
mean = stat.mean(data)
median = stat.median(data)
mode = stat.mode(data)
std_deviation = stat.stdev(data)

#finding 1 standard deviation start and end values,2 standard deviation start and end values and 3 standard deviation start and end values
first_standard_deviation_start,first_standard_deviation_end = mean-std_deviation,mean+std_deviation
second_standard_deviation_start,second_standard_deviation_end = mean-(2*std_deviation),mean+(2*std_deviation)
third_standard_deviation_start,third_standard_deviation_end = mean-(3*std_deviation),mean+(3*std_deviation)

#Printing the findings
list_of_data_within_1_std_deviation = [result for result in data if result > first_standard_deviation_start and result < first_standard_deviation_end]
list_of_data_within_2_std_deviation = [result for result in data if result > second_standard_deviation_start and result < second_standard_deviation_end]
list_of_data_within_3_std_deviation = [result for result in data if result > third_standard_deviation_start and result < third_standard_deviation_end]

#acutally printing them
print("Mean of this data is {}".format(mean))
print("Median of this data is {}".format(median))
print("Mode of this data is {}".format(mode))
print("Standard deviation of this data is {}".format(std_deviation))

#Printing and calculating standard deviation in percentage
print("{}% of data lies within 1 standard deviation".format(len(list_of_data_within_1_std_deviation)*100.0/len(data)))
print("{}% of data lies within 2 standard deviation".format(len(list_of_data_within_2_std_deviation)*100.0/len(data)))
print("{}% of data lies within 3 standard deviation".format(len(list_of_data_within_3_std_deviation)*100.0/len(data)))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec_()