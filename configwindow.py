import pdb
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QMessageBox,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QFileDialog,
)

from grid import Grid
from world import World
from gamewindow import GameWindow
from helpwindow import HelpWindow
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class CreateStateWindow(QWidget):
    """A window for creating the initial state in Game of Life."""
    def __init__(self, grid: Grid) -> None:
        """Create a new state creation window.

        Args:
            grid: the grid to use for the initial state.
        """
        super().__init__()
        self.setWindowTitle("Create initial state")
        self._grid = grid
        layout = QGridLayout()
        self._create_mpl_figure()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._save_clicked)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._reset_clicked)
        layout.addWidget(self._canvas, 0, 0, 1, 2)
        layout.addWidget(self.save_button, 1, 0, 1, 1)
        layout.addWidget(self.reset_button, 1, 1, 1, 1)
        self.setLayout(layout)
        self.show()

    def _create_mpl_figure(self) -> None:
        """Create the matplotlib figure for creating the state."""
        plt.figure()
        ax = plt.axes(xticks=[], yticks=[])
        self._im = ax.imshow(self._grid.cells, cmap="binary", vmin=0, vmax=1)
        self._canvas = FigureCanvasQTAgg(ax.figure)
        self._canvas.mpl_connect("button_press_event", self._on_canvas_clicked)

    def _on_canvas_clicked(self, event) -> None:
        """To be executed when a grid cell is de/selected."""
        if event.inaxes is self._im.axes:
            data = self._im.get_array()
            j, i = int(event.xdata + 0.5), int(event.ydata + 0.5)
            data[i, j] = not data[i, j]
            self._grid.cells[i, j] = not self._grid.cells[i, j]
            self._im.set_array(data)
            event.canvas.draw()

    def _save_clicked(self) -> None:
        """Save the current state to file."""
        fname, _ = QFileDialog().getSaveFileName(self)
        if fname == "":
            return
        np.savetxt(fname, self._im.get_array(), fmt="%d")

    def _reset_clicked(self) -> None:
        """Reset to a clean state with all cells deselected."""
        self._grid.clear()
        self._im.set_array(self._grid.cells)
        self._canvas.draw()

    def closeEvent(self, event) -> None:
        """Close the matplotlib figure for creating the state."""
        plt.close()


class WorldPropertiesPanel(QGroupBox):
    """A panel for setting the world properties."""
    def __init__(self, world: World) -> None:
        """Create a new panel for setting the world properties.

        Args:
            world: the world whose properties are being set.
        """
        super().__init__("World Properties")
        self._world = world

        layout = QGridLayout()
        layout.addWidget(
            QLabel("Define world", alignment=Qt.AlignmentFlag.AlignCenter), 0, 0, 1, 2
        )
        layout.addWidget(QLabel("Height", alignment=Qt.AlignmentFlag.AlignCenter), 1, 0)
        layout.addWidget(QLabel("Width", alignment=Qt.AlignmentFlag.AlignCenter), 1, 1)
        self.height_box = QLineEdit(
            f"{self._world.height}", alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.height_box.editingFinished.connect(self._height_changed)
        self.width_box = QLineEdit(
            f"{self._world.width}", alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.width_box.editingFinished.connect(self._width_changed)
        layout.addWidget(self.height_box, 2, 0)
        layout.addWidget(self.width_box, 2, 1)
        layout.addWidget(QLabel(), 3, 0)
        layout.addWidget(
            QLabel("Choose boundary condition", alignment=Qt.AlignmentFlag.AlignCenter),
            4,
            0,
            1,
            2,
        )
        self.bc_box = QComboBox()
        self.bc_box.addItems(["Hard wall", "Periodic"])
        self.bc_box.currentIndexChanged.connect(self._bc_changed)
        layout.addWidget(self.bc_box, 5, 0, 1, 2)

        self.setLayout(layout)

    def _height_changed(self) -> None:
        """To be executed when the world height is changed."""
        new_height = int(self.height_box.text())
        if new_height <= 0:
            QMessageBox(text="Height must be greater than 0.").exec()
            self.height_box.setText(f"{self._world.height}")
        else:
            self._world.height = new_height
            if self._world.ic is not None:
                if self._world.ic.ny != new_height:
                    self._world.ic.cells = np.zeros(
                        (new_height, int(self._world.width))
                    )

    def _width_changed(self) -> None:
        """To be executed when the world width is changed."""
        new_width = int(self.width_box.text())
        if new_width <= 0:
            QMessageBox(text="Width must be greater than 0.").exec()
            self.width_box.setText(f"{self._world.width}")
        else:
            self._world.width = new_width
            if self._world.ic is not None:
                if self._world.ic.nx != new_width:
                    self._world.ic.cells = np.zeros(
                        (int(self._world.height), new_width)
                    )

    def _bc_changed(self) -> None:
        """To be executed when the world boundary conditions are changed."""
        self._world.bc = self.bc_box.currentText()


class InitialConditionsPanel(QGroupBox):
    """A panel for setting the worlds' initial conditions."""
    def __init__(self, world: World) -> None:
        """Create a new panel for setting the world's initial conditions.

        Args:
            world: the world whose initial conditions are being set.
        """
        super().__init__("Initial Conditions")
        self._world = world

        layout = QVBoxLayout()
        sublayout = QHBoxLayout()
        sublayout_wid = QWidget()

        self.cbox = QCheckBox("Random state")
        self.cbox.stateChanged.connect(self._random_state_toggled)
        cs_btn = QPushButton("Create state")
        cs_btn.clicked.connect(self.create_state)
        ls_btn = QPushButton("Load state")
        ls_btn.clicked.connect(self.open_state)

        layout.addWidget(self.cbox)
        sublayout.addWidget(cs_btn)
        sublayout.addWidget(ls_btn)
        sublayout_wid.setLayout(sublayout)
        layout.addWidget(sublayout_wid)

        self.setLayout(layout)

    def _random_state_toggled(self) -> None:
        """To be executed when the random state checkbox is un/checked."""
        if self.cbox.isChecked():
            grid = Grid(
                cells=np.random.randint(
                    0, 2, (int(self._world.height), int(self._world.width))
                )
            )
            self._world.ic = grid

    def open_state(self) -> None:
        """Open a saved state from file."""
        fname, _ = QFileDialog().getOpenFileName(self)
        if fname == "":
            return
        cells = np.loadtxt(fname, dtype=int)
        grid = Grid(cells=cells)
        self._world.ic = grid
        self.cbox.setChecked(False)
        self.parent().parent().wp.height_box.setText(f"{grid.ny}")
        self.parent().parent().wp.width_box.setText(f"{grid.nx}")

    def create_state(self) -> None:
        """Manually create a new state."""
        if self._world.ic is None:
            self._world.ic = Grid(
                    cells=np.zeros((int(self._world.height), int(self._world.width)))
                )
        self.create_state_window = CreateStateWindow(self._world.ic)


class GameRulesPanel(QGroupBox):
    """A panel for setting the game rules."""
    def __init__(self, world: World) -> None:
        """Create a new panel for setting the game rules.

        Args:
            world: the world in the game whose rules are being set.
        """
        super().__init__("Game Rules")
        self._world = world

        layout = QGridLayout()
        self.tbox1 = QLineEdit("2")
        self.tbox2 = QLineEdit("3")
        self.tbox3 = QLineEdit("3")

        checkbox = QCheckBox("Use default")
        checkbox.clicked.connect(self._use_default_rules)
        layout.addWidget(checkbox, 0, 0)
        layout.addWidget(QLabel("Cell dies if it has <"), 1, 0)
        layout.addWidget(QLabel("Cell dies if it has >"), 2, 0)
        layout.addWidget(QLabel("Cell born if it has"), 3, 0)
        layout.addWidget(self.tbox1, 1, 1)
        layout.addWidget(self.tbox2, 2, 1)
        layout.addWidget(self.tbox3, 3, 1)
        self.tbox1.editingFinished.connect(self._rules_changed)
        self.tbox2.editingFinished.connect(self._rules_changed)
        self.tbox3.editingFinished.connect(self._rules_changed)
        layout.addWidget(QLabel("live neighbours"), 1, 2)
        layout.addWidget(QLabel("live neighbours"), 2, 2)
        layout.addWidget(QLabel("live neighbours"), 3, 2)

        self.setLayout(layout)

    def _rules_changed(self) -> None:
        """To be executed when the rules are changed."""
        if (
            int(self.tbox1.text()) <= 0
            or int(self.tbox2.text()) <= 0
            or int(self.tbox3.text()) <= 0
        ):
            QMessageBox(text="Number of neighbours must be greater than or equal to 0.").exec()
        else:
            self._world.rules = [
                int(self.tbox1.text()), int(self.tbox2.text()), int(self.tbox3.text())
            ]

    def _use_default_rules(self, val) -> None:
        """Use the default Game of Life rules."""
        self.tbox1.setEnabled(not val)
        self.tbox2.setEnabled(not val)
        self.tbox3.setEnabled(not val)
        if val:
            self.tbox1.setText("2")
            self.tbox2.setText("3")
            self.tbox3.setText("3")
            self._rules_changed()


class MainWindow(QMainWindow):
    """The main window for configuring Game of Life."""
    def __init__(self) -> None:
        """Create a new main window."""
        super().__init__()
        self.setWindowTitle("Game of Life setup")
        self.resize(600, 400)

        self.world = World()
        layout = QGridLayout()

        # Create subframes
        self.wp = WorldPropertiesPanel(self.world)
        self.ic = InitialConditionsPanel(self.world)
        self.gr = GameRulesPanel(self.world)

        h_btn = QPushButton("Help")
        h_btn.clicked.connect(self._help_clicked)
        layout.addWidget(h_btn, 0, 2)
        layout.addWidget(self.wp, 1, 0)
        layout.addWidget(self.ic, 1, 1, 1, 2)
        layout.addWidget(self.gr, 2, 0)

        # Create final subframe with tick length and play button
        tp_layout = QVBoxLayout()
        tp_layout_wid = QWidget()
        tp_sublayout = QHBoxLayout()
        tp_sublayout_wid = QWidget()

        self.t_tbox = QLineEdit(f"{self.world.tick}")
        self.t_tbox.editingFinished.connect(self._tick_changed)
        tp_sublayout.addWidget(QLabel("Set tick"))
        tp_sublayout.addWidget(self.t_tbox)

        p_btn = QPushButton("Play")
        p_btn.clicked.connect(self._play_clicked)
        tp_sublayout_wid.setLayout(tp_sublayout)

        tp_layout.addWidget(tp_sublayout_wid)
        tp_layout.addWidget(p_btn)

        tp_layout_wid.setLayout(tp_layout)
        layout.addWidget(tp_layout_wid, 2, 1, 1, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def _tick_changed(self) -> None:
        """To be executed when the tick is changed."""
        new_tick = float(self.t_tbox.text())
        if new_tick <= 0:
            QMessageBox(text="Tick length must be greater than 0.").exec()
            self.t_tbox.setText(f"{self.world.tick}")
        else:
            self.world.tick = new_tick

    def _help_clicked(self) -> None:
        self.help_window = HelpWindow()
        self.help_window.show()

    def _play_clicked(self) -> None:
        """Begin the Game of Life."""
        print("Using the following settings:")
        print(f"{self.world.height} height")
        print(f"{self.world.width} width")
        print(f"{self.world.bc} boundary conditions")
        print(f"{self.world.rules} rules")
        print(f"{self.world.tick} tick")
        if self.world.ic is None:
            print("No grid set")
        self.game_window = GameWindow(self.world)
