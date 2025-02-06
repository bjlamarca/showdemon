from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt


class ChartTest(QChartView):
    def __init__(self):
        super().__init__()
    # Create a QChart object
        chart = QChart()
        chart.setTitle("Line Chart Example")

        # Create a QLineSeries object
        series = QLineSeries()
        series.setName("Data Series")
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)

        # Add the series to the chart
        chart.addSeries(series)

        # Create axes
        x_axis = QValueAxis()
        x_axis.setTitleText("X-Axis")
        chart.addAxis(x_axis, Qt.AlignBottom)
        series.attachAxis(x_axis)

        y_axis = QValueAxis()
        y_axis.setTitleText("Y-Axis")
        chart.addAxis(y_axis, Qt.AlignLeft)
        series.attachAxis(y_axis)

        self.setChart(chart)