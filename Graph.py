import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import matplotlib.pyplot as plt

class Graph(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()



        self.fig = plt.figure()
        self.axis1 = self.fig.add_subplot(1,1,1)

        self.title = "Price"

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(400, 300)
        self.add(self.canvas)

    def plot_date_axis_1(self, x_vals, y_vals):
        self.axis1.clear()
        self.axis1.plot_date(x_vals, y_vals, linestyle="solid")
        self.axis1.set_title(self.title)
        self.axis1.set_ylabel("Price (£)")
        self.axis1.set_xlabel("Date")
        self.redraw()

    def redraw(self):
        self.remove(self.canvas)
        self.add(self.canvas)