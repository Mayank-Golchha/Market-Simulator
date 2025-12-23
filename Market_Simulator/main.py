import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
                             QPushButton,QDialog,QLabel,QLineEdit,QTableWidget, QTableWidgetItem,QHeaderView)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor
import pyqtgraph as pg

from Simulator import Simulation
import data

#
# class OrderWindow(QDialog):
#     # for user to place orders
#     def __init__(self, order_type, callback):
#         super().__init__()
#         self.setWindowTitle(f"{order_type} Order")
#         self.order_type = order_type
#         self.callback = callback
#
#         layout = QVBoxLayout()
#
#         layout.addWidget(QLabel(f"Enter Quantity to {order_type}:"))
#
#         self.qty_input = QLineEdit()
#         self.qty_input.setPlaceholderText("Quantity")
#         layout.addWidget(self.qty_input)
#
#         # Submit button
#         btn = QPushButton("Submit")
#         btn.clicked.connect(self.submit)
#         layout.addWidget(btn)
#
#         self.setLayout(layout)
#         self.setFixedSize(250, 120)
#
#     def submit(self):
#         qty_text = self.qty_input.text()
#
#         if qty_text.isdigit():
#             qty = int(qty_text)
#             self.callback(self.order_type, qty)
#             self.close()
#         else:
#             self.qty_input.setText("")
#             self.qty_input.setPlaceholderText("Invalid quantity")
#
#

class Level2Window(QDialog):
    def __init__(self, n_rows=10):
        super().__init__()
        self.setWindowTitle("Level 2 Data")
        self.setMinimumSize(400, 300)
        self.n_rows = n_rows

        layout = QVBoxLayout()

        title = QLabel("Level2 Data")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(title)

        # Table with n rows
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Buy Price, Buy Volume, Sell Price, Sell Volume
        self.table.setRowCount(self.n_rows)
        self.table.setHorizontalHeaderLabels(["Buy Price", "Buy Volume", "Sell Price", "Sell Volume"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def update_table(self, buy_orders : dict,buy_prices : list, sell_orders : dict,sell_prices : list):
        for i in range(self.n_rows):
            # Buy side
            if i < len(buy_orders):
                price = buy_prices[len(buy_prices) - i - 1]
                volume = buy_orders[price]
                self.table.setItem(i, 0, QTableWidgetItem(f"{price:.2f}"))
                self.table.setItem(i, 1, QTableWidgetItem(str(volume)))
            else:
                self.table.setItem(i, 0, QTableWidgetItem(""))
                self.table.setItem(i, 1, QTableWidgetItem(""))

            # Sell side
            if i < len(sell_orders):
                # price, vol = sell_orders[i]
                price = sell_prices[i]
                volume = sell_orders[price]
                self.table.setItem(i, 2, QTableWidgetItem(f"{price:.2f}"))
                self.table.setItem(i, 3, QTableWidgetItem(str(volume)))
            else:
                self.table.setItem(i, 2, QTableWidgetItem(""))
                self.table.setItem(i, 3, QTableWidgetItem(""))


class FilledOrderWindow(QDialog):
    # to show all filled orders by exchange
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Filled Orders")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()

        title = QLabel("All Filled Orders")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 8px;")
        layout.addWidget(title)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Buyer ID", "Seller ID", "Price", "Quantity", "Time"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def update_table(self, transactions):
        self.table.setRowCount(len(transactions))

        for row, t in enumerate(transactions):
            self.table.setItem(row, 0, QTableWidgetItem(str(t.buyer_id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(t.seller_id)))
            self.table.setItem(row, 2, QTableWidgetItem(f"{t.price:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(str(t.quantity)))
            self.table.setItem(row, 4, QTableWidgetItem(str(t.time)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Market Simulator")
        self.setGeometry(100, 100, 1000, 700)

        self.simulator = Simulation(data.STARTING_PRICE)

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # filled order window
        self.filled_window = FilledOrderWindow()

        # level2 data window
        self.level2_window = Level2Window(n_rows=data.WINDOW_LEVEL2_MAX_ROWS)

        # menu bar
        menu_bar = self.menuBar()
        view_menu = menu_bar.addMenu("View")
        filled_order_view = view_menu.addAction("Filled Order")
        level2_data_view = view_menu.addAction("Level2 Data")

        filled_order_view.triggered.connect(self.show_filled_order)
        level2_data_view.triggered.connect(self.show_level2_window)

        button_layout = QHBoxLayout()

        # buy_btn = QPushButton("BUY")
        # sell_btn = QPushButton("SELL")
        self.price_label = QLabel(f"Price: {self.simulator.starting_price:.2f}")
        self.price_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        # buy_btn.setFixedWidth(80)
        # sell_btn.setFixedWidth(80)
        self.price_label.setFixedWidth(200)

        self.order_window = None

        # buy_btn.clicked.connect(self.buy_window)
        # sell_btn.clicked.connect(self.sell_window)

        # button_layout.addWidget(buy_btn)
        button_layout.addWidget(self.price_label)
        # button_layout.addWidget(sell_btn)

        self.layout.addLayout(button_layout)

        self.plot_widget = pg.PlotWidget()

        self.layout.addWidget(self.plot_widget)

        # self.plot_widget.setXRange(0, 25)  # Show first 20 candles by default

        # self.plot_widget.setMouseEnabled(x=True, y=True)  # allow horizontal scroll
        # self.plot_widget.showGrid(x=True, y=True)
        # self.plot_widget.setBackground('w')

        # vb = self.plot_widget.getViewBox()
        # vb.setLimits(xMin=0)  # don't scroll past 0
        # xMax is not set, so you can scroll infinitely to the right
        self.plot_widget.setMouseEnabled(x=True, y=True)

        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setBackground('w')
        self.plot_widget.setTitle("Market Simulator")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(500)


    # def buy_window(self):
    #     # self.order_window = OrderWindow("BUY", self.handle_order)
    #     # self.order_window.exec()
    #     # self.simulator.company.place_order(100,self.simulator.company.place_buy_order(self.simulator.exchange.price * 1.05, 1000))
    #     # self.simulator.company.place_buy_order(102, 10000)
    #     # print("Company Bought")
    #     pass
    #
    # def sell_window(self):
    #     # self.order_window = OrderWindow("SELL", self.handle_order)
    #     # self.order_window.exec()
    #     # if self.simulator.company.holdings >= 1000:
    #     #     self.simulator.company.place_order(100,self.simulator.company.place_sell_order(self.simulator.exchange.price * 0.98,1000))
    #     #     self.simulator.company.place_sell_order(105,10000)
    #         # print("Company Sold")
    #     pass


    def show_filled_order(self):
        self.filled_window.show()

    def show_level2_window(self):
        self.level2_window.show()

    def update_plot(self):
        self.simulator.next_candle()

        if self.filled_window.isVisible():
            self.filled_window.update_table(self.simulator.exchange.completed_order)

        if self.level2_window.isVisible():
            self.level2_window.update_table(self.simulator.exchange.level_2_data.buy_data,self.simulator.exchange.level_2_data.buy_prices,
                            self.simulator.exchange.level_2_data.sell_data,self.simulator.exchange.level_2_data.sell_prices)

        self.plot_widget.clear()

        candles = self.simulator.candles
        # self.plot_widget.setXRange(0, len(candles) + 5)

        last_price = candles[-1].Close
        self.price_label.setText(f"Price: {last_price:.2f}")

        # width = 1
        width = 0.9
        for i, candle in enumerate(candles):
            open_price = candle.Open
            high_price = candle.High
            low_price = candle.Low
            close_price = candle.Close
            color = QColor(0, 180, 0) if close_price >= open_price else QColor(200, 0, 0)

            x = i + 0.5

            # wick
            self.plot_widget.plot([x, x], [low_price, high_price],pen=pg.mkPen(color, width=2))
            # body
            body_height = abs(close_price - open_price)
            y0 = min(open_price, close_price)
            bar = pg.BarGraphItem(x = [x],height = [body_height],width = width,y0 = y0,brush = color)
            self.plot_widget.addItem(bar)

        # self.plot_widget.getViewBox().setLimits(xMin=0)  # can't scroll left past 0
        self.plot_widget.setMouseEnabled(x=True, y=True)

        # self.plot_widget.setXRange(max(0,len(candles)-15), 15)
        # self.plot_widget.setXRange(max(0, len(candles)-15), len(candles))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
