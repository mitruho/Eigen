import numpy as np
from gi.repository import Gtk, Gdk, Adw, Gio
from .matrix_view import MatrixView
from .matrix_data import MatrixData
from .decomposition_handler import DecompositionHandler
from .size_handler import SizeHandler

@Gtk.Template(resource_path='/com/github/elahpeca/Eigen/gtk/window.ui')
class EigenWindow(Adw.ApplicationWindow):
    """
    Main application window for Eigen.

    Handles the user interface and interaction with matrix data.
    """
    __gtype_name__ = 'EigenWindow'

    main_content = Gtk.Template.Child()
    decomposition_dropdown = Gtk.Template.Child()
    matrix_control_box = Gtk.Template.Child()
    matrix_control_box2   = Gtk.Template.Child()
    rows_dropdown = Gtk.Template.Child()
    cols_dropdown = Gtk.Template.Child()
    rows_dropdown2 = Gtk.Template.Child()
    cols_dropdown2 = Gtk.Template.Child()
    matrix_copy_button = Gtk.Template.Child()
    matrix_cleanup_button = Gtk.Template.Child()
    additional_content = Gtk.Template.Child()
    decompose_button = Gtk.Template.Child()
    def __init__(self, **kwargs):
        """
        Initializes the EigenWindow.

        Args:
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(**kwargs)
        self.settings = Gio.Settings.new('com.github.elahpeca.Eigen')
        self.connect('unrealize', self.save_window_properties)

        self.decomposition_handler = DecompositionHandler(self.decomposition_dropdown)
        self.size_handler = SizeHandler(self.rows_dropdown, self.cols_dropdown)
        self.size_handler2 = SizeHandler(self.rows_dropdown2, self.cols_dropdown2)

        self.update_matrix_size()
        self.setup_matrix_view()

        self.rows_dropdown.connect('notify::selected', self.on_size_changed)
        self.cols_dropdown.connect('notify::selected', self.on_size_changed)
        self.rows_dropdown2.connect('notify::selected', self.on_size_changed2)
        self.cols_dropdown2.connect('notify::selected', self.on_size_changed2)
        self.matrix_cleanup_button.connect('clicked', self.on_matrix_cleanup_clicked)
        self.matrix_copy_button.connect('clicked', self.on_matrix_copy_clicked)
        self.decompose_button.connect('clicked', self.on_decompose_clicked)
        self.decomposition_dropdown.connect("notify::selected", self.on_decomposition_changed)
        self.on_decomposition_changed()

    def save_window_properties(self, *args):
        """
        Save window size to settings when it is unrealized (closed).

        Args:
            *args: Positional arguments passed by the signal.
        """
        window_size = self.get_default_size()
        self.settings.set_int('window-width', window_size.width)
        self.settings.set_int('window-height', window_size.height)

    def setup_matrix_view(self):
        """
        Creates a MatrixView instance, configures its appearance
        and binds it to the matrix data.
        """
        self.matrix_view = MatrixView()
        self.matrix_view.set_row_homogeneous(True)
        self.matrix_view.set_column_homogeneous(True)
        self.matrix_view.set_row_spacing(5)
        self.matrix_view.set_column_spacing(5)
        self.main_content.insert_child_after(self.matrix_view, self.decomposition_dropdown)

        self.matrix_data = MatrixData(self.current_rows, self.current_cols)
        self.matrix_view.set_matrix(self.matrix_data)

    def update_matrix_size(self):
        """Update internal row and column counts based on dropdown selection."""
        self.current_rows, self.current_cols = self.size_handler.get_selected_size()
    def update_matrix2_size(self):
        """Update internal row and column counts based on dropdown selection."""
        self.current_rows2, self.current_cols2 = self.size_handler2.get_selected_size()

    def on_size_changed(self, *args):
        """
        Handle changes in matrix size dropdowns.

        Args:
            *args: Positional arguments passed by the signal.
        """
        self.update_matrix_size()
        self.matrix_data.resize(self.current_rows, self.current_cols)
        self.matrix_view.set_matrix(self.matrix_data)

    def on_size_changed2(self, *args):
        """
        Handle changes in matrix size dropdowns.

        Args:
            *args: Positional arguments passed by the signal.
        """
        self.update_matrix2_size()
        self.matrix_data2.resize(self.current_rows2, self.current_cols2)
        self.matrix_view2.set_matrix(self.matrix_data2)

    def on_matrix_copy_clicked(self, button):
        """
        Handle the event when the matrix copy button is clicked.

        Args:
            button: The button that triggered the event.
        """
        display = Gdk.Display.get_default()
        clipboard = display.get_clipboard()
        content_provider = Gdk.ContentProvider.new_for_value(str(self.matrix_data.data))
        clipboard.set_content(content_provider)

    def on_decompose_clicked(self, button):
        w, v = np.linalg.eig(self.matrix_data.data)    # find eigenvalues and eigenvectors
        print(f'eigenvalues = {w}')    # each entry is an eigenvalue
        print(f'eigenvectors = \n{v}')    # each column is the corresponding eigenvector

    def on_matrix_cleanup_clicked(self, button):
        """
        Clear the matrix when cleanup button is clicked.

        Args:
            button: The button that triggered the event.
        """
        self.matrix_view.clear_matrix(self.current_rows, self.current_cols)
    def on_decomposition_changed(self, *args):
        choice = self.decomposition_handler.get_selected_key()   # 0 or 1 :contentReference[oaicite:1]{index=1}
        self.matrix_control_box2.set_visible(choice == 0)

    # ---------- create ----------
        if choice == 0 and not hasattr(self, "matrix_view2"):
            self.matrix_view2 = MatrixView()
            self.matrix_view2.set_row_homogeneous(True)
            self.matrix_view2.set_column_homogeneous(True)
            self.matrix_view2.set_row_spacing(5)
            self.matrix_view2.set_column_spacing(5)

        # insert directly under the first matrix
            self.additional_content.append(self.matrix_view2)

            self.matrix_data2 = MatrixData(self.current_rows, self.current_cols)
            self.matrix_view2.set_matrix(self.matrix_data2)

    # ---------- remove ----------
        elif choice != 0 and hasattr(self, "matrix_view2"):
            self.matrix_view2.unparent()      # or self.main_content.remove(...)
            del self.matrix_view2              # <— make the attribute disappear
            del self.matrix_data2

