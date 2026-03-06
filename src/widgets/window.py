import ast
import numpy as np
from gi.repository import Gtk, Gdk, Adw, Gio
from .matrix_view import MatrixView
from .matrix_data import MatrixData
from .mode_handler import ModeHandler
from .size_handler import SizeHandler
from .op_handler import OpHandler
from .result_window import ResultWindow, CalcResultDialog, QRResultWindow

@Gtk.Template(resource_path='/com/github/elahpeca/Eigen/gtk/window.ui')
class EigenWindow(Adw.ApplicationWindow):
    """
    Main application window for Eigen.

    Handles the user interface and interaction with matrix data.
    """
    __gtype_name__ = 'EigenWindow'

    matrix_menu_main = Gtk.Template.Child()
    matrices_box = Gtk.Template.Child()
    mode_dropdown = Gtk.Template.Child()
    op_dropdown = Gtk.Template.Child()
    op_dropdown_box = Gtk.Template.Child()
    matrix_control_box_main = Gtk.Template.Child()
    matrix_control_box_2   = Gtk.Template.Child()
    rows_dropdown_main = Gtk.Template.Child()
    cols_dropdown_main = Gtk.Template.Child()
    rows_dropdown_2 = Gtk.Template.Child()
    cols_dropdown_2 = Gtk.Template.Child()
    action_panel_main = Gtk.Template.Child()
    action_panel_2 = Gtk.Template.Child()
    matrix_transpose_button_main = Gtk.Template.Child()
    matrix_invert_button_main = Gtk.Template.Child()
    matrix_copy_button_main = Gtk.Template.Child()
    matrix_paste_button_main = Gtk.Template.Child()
    matrix_cleanup_button_main = Gtk.Template.Child()
    matrix_transpose_button_2 = Gtk.Template.Child()
    matrix_invert_button_2 = Gtk.Template.Child()
    matrix_copy_button_2 = Gtk.Template.Child()
    matrix_paste_button_2 = Gtk.Template.Child()
    matrix_cleanup_button_2 = Gtk.Template.Child()
    matrix_menu_2 = Gtk.Template.Child()
    execute_button = Gtk.Template.Child()
    def __init__(self, **kwargs):
        """
        Initializes the EigenWindow.

        Args:
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        super().__init__(**kwargs)
        self.settings = Gio.Settings.new('com.github.elahpeca.Eigen')
        self.connect('unrealize', self.save_window_properties)

        self.mode_handler = ModeHandler(self.mode_dropdown)
        self.size_handler = SizeHandler(self.rows_dropdown_main, self.cols_dropdown_main)
        self.size_handler2 = SizeHandler(self.rows_dropdown_2, self.cols_dropdown_2)
        self.op_handler = OpHandler(self.op_dropdown)
        self.update_matrix_size()
        self.update_matrix2_size()
        self.setup_matrix_view()

        self._rows_handler = self.rows_dropdown_main.connect('notify::selected', self.on_size_changed)
        self._cols_handler = self.cols_dropdown_main.connect('notify::selected', self.on_size_changed)
        self._rows2_handler = self.rows_dropdown_2.connect('notify::selected', self.on_size_changed2)
        self._cols2_handler = self.cols_dropdown_2.connect('notify::selected', self.on_size_changed2)
        self.matrix_cleanup_button_main.connect('clicked', self.on_matrix_cleanup_clicked)
        self.matrix_copy_button_main.connect('clicked', self.on_matrix_copy_clicked)
        self.matrix_paste_button_main.connect('clicked', self.on_matrix_paste_clicked)
        self.matrix_transpose_button_main.connect('clicked', self.on_matrix_transpose_clicked)
        self.matrix_invert_button_main.connect('clicked', self.on_matrix_invert_clicked)
        self.matrix_cleanup_button_2.connect('clicked', self.on_matrix_cleanup2_clicked)
        self.matrix_copy_button_2.connect('clicked', self.on_matrix_copy2_clicked)
        self.matrix_paste_button_2.connect('clicked', self.on_matrix_paste2_clicked)
        self.matrix_transpose_button_2.connect('clicked', self.on_matrix_transpose2_clicked)
        self.matrix_invert_button_2.connect('clicked', self.on_matrix_invert2_clicked)
        self.execute_button.connect('clicked', self.on_execute_clicked)
        self.mode_dropdown.connect("notify::selected", self.on_decomposition_changed)
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
        self.matrix_view.set_halign(Gtk.Align.CENTER)
        self.matrix_menu_main.insert_child_after(self.matrix_view, self.matrix_control_box_main)

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

    def _parse_matrix_text(self, text):
        """Parse clipboard text into a 2D list of floats, or return None on failure."""
        if not text or not text.strip():
            return None
        # Try Python list format (our own copy format)
        try:
            data = ast.literal_eval(text.strip())
            if (isinstance(data, list) and data and
                    all(isinstance(row, list) and row for row in data) and
                    all(isinstance(v, (int, float)) for row in data for v in row)):
                row_len = len(data[0])
                if all(len(row) == row_len for row in data):
                    return [[float(v) for v in row] for row in data]
        except (ValueError, SyntaxError):
            pass

    def on_matrix_paste_clicked(self, button):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.read_text_async(None, self._on_paste_text_ready)

    def _on_paste_text_ready(self, clipboard, result):
        text = clipboard.read_text_finish(result)
        data = self._parse_matrix_text(text)
        if data is None:
            return
        new_rows, new_cols = len(data), len(data[0])
        if new_rows > 7 or new_cols > 7:
            return
        self.rows_dropdown_main.handler_block(self._rows_handler)
        self.cols_dropdown_main.handler_block(self._cols_handler)
        self.rows_dropdown_main.set_selected(new_rows - 1)
        self.cols_dropdown_main.set_selected(new_cols - 1)
        self.rows_dropdown_main.handler_unblock(self._rows_handler)
        self.cols_dropdown_main.handler_unblock(self._cols_handler)
        self.matrix_data.rows = new_rows
        self.matrix_data.cols = new_cols
        self.matrix_data.data = data
        self.current_rows, self.current_cols = new_rows, new_cols
        self.matrix_view.set_matrix(self.matrix_data)
        self.matrix_view.load_matrix_values()

    def on_matrix_paste2_clicked(self, button):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.read_text_async(None, self._on_paste2_text_ready)

    def _on_paste2_text_ready(self, clipboard, result):
        text = clipboard.read_text_finish(result)
        data = self._parse_matrix_text(text)
        if data is None:
            return
        new_rows, new_cols = len(data), len(data[0])
        if new_rows > 7 or new_cols > 7:
            return
        self.rows_dropdown_2.handler_block(self._rows2_handler)
        self.cols_dropdown_2.handler_block(self._cols2_handler)
        self.rows_dropdown_2.set_selected(new_rows - 1)
        self.cols_dropdown_2.set_selected(new_cols - 1)
        self.rows_dropdown_2.handler_unblock(self._rows2_handler)
        self.cols_dropdown_2.handler_unblock(self._cols2_handler)
        self.matrix_data2.rows = new_rows
        self.matrix_data2.cols = new_cols
        self.matrix_data2.data = data
        self.current_rows2, self.current_cols2 = new_rows, new_cols
        self.matrix_view2.set_matrix(self.matrix_data2)
        self.matrix_view2.load_matrix_values()



    def on_execute_clicked(self, button):
        if self.mode_handler.get_selected_key() == 0:
            self._run_calculator()
        elif self.mode_handler.get_selected_key() == 1:
            try:
                self.eigenvalues, self.eigenvectors = np.linalg.eig(self.matrix_data.data)
            except ValueError:
                dialog = Adw.AlertDialog(heading="Error!", body="Operation not applicable.")
                dialog.add_response("ok", "OK")
                dialog.present(self)
                return
            ResultWindow(self.eigenvalues, self.eigenvectors).present(self)
        elif self.mode_handler.get_selected_key() == 2:
            try:
                self.orthonormal, self.upper_trian = np.linalg.qr(self.matrix_data.data)
            except ValueError:
                dialog = Adw.AlertDialog(heading="Error!", body="Operation not applicable.")
                dialog.add_response("ok", "OK")
                dialog.present(self)
                return

            QRResultWindow(self.orthonormal, self.upper_trian).present(self)

    def _run_calculator(self):
        A = np.array(self.matrix_data.data)
        B = np.array(self.matrix_data2.data)
        op = self.op_handler.get_selected_op()
        try:
            if op == 0:
                result = A + B
            elif op == 1:
                result = A - B
            else:
                if A.shape == (1, 1):
                    result = A[0, 0] * B
                elif B.shape == (1, 1):
                    result = A * B[0, 0]
                else:
                    result = A @ B
        except ValueError:
            dialog = Adw.AlertDialog(heading="Error!", body="Operation not applicable.")
            dialog.add_response("ok", "OK")
            dialog.present(self)
            return
        CalcResultDialog(result).present(self)

    def on_matrix_cleanup_clicked(self, button):
        """
        Clear the matrix when cleanup button is clicked.

        Args:
            button: The button that triggered the event.
        """
        self.matrix_view.clear_matrix(self.current_rows, self.current_cols)

    def on_matrix_copy2_clicked(self, button):
        display = Gdk.Display.get_default()
        clipboard = display.get_clipboard()
        content_provider = Gdk.ContentProvider.new_for_value(str(self.matrix_data2.data))
        clipboard.set_content(content_provider)

    def on_matrix_cleanup2_clicked(self, button):
        self.matrix_view2.clear_matrix(self.current_rows2, self.current_cols2)

    def on_matrix_transpose2_clicked(self, button):
        transposed = np.array(self.matrix_data2.data).T
        new_rows, new_cols = transposed.shape

        self.rows_dropdown_2.handler_block(self._rows2_handler)
        self.cols_dropdown_2.handler_block(self._cols2_handler)
        self.rows_dropdown_2.set_selected(new_rows - 1)
        self.cols_dropdown_2.set_selected(new_cols - 1)
        self.rows_dropdown_2.handler_unblock(self._rows2_handler)
        self.cols_dropdown_2.handler_unblock(self._cols2_handler)

        self.matrix_data2.rows = new_rows
        self.matrix_data2.cols = new_cols
        self.matrix_data2.data = transposed.tolist()
        self.current_rows2, self.current_cols2 = new_rows, new_cols
        self.matrix_view2.set_matrix(self.matrix_data2)
        self.matrix_view2.load_matrix_values()

    def on_matrix_transpose_clicked(self, button):
        transposed = np.array(self.matrix_data.data).T
        new_rows, new_cols = transposed.shape

        self.rows_dropdown_main.handler_block(self._rows_handler)
        self.cols_dropdown_main.handler_block(self._cols_handler)
        self.rows_dropdown_main.set_selected(new_rows - 1)
        self.cols_dropdown_main.set_selected(new_cols - 1)
        self.rows_dropdown_main.handler_unblock(self._rows_handler)
        self.cols_dropdown_main.handler_unblock(self._cols_handler)

        self.matrix_data.rows = new_rows
        self.matrix_data.cols = new_cols
        self.matrix_data.data = transposed.tolist()
        self.current_rows, self.current_cols = new_rows, new_cols
        self.matrix_view.set_matrix(self.matrix_data)
        self.matrix_view.load_matrix_values()

    def on_matrix_invert_clicked(self, button):
        M = np.array(self.matrix_data.data)
        try:
            inverted = np.linalg.inv(M)
        except np.linalg.LinAlgError:
            dialog = Adw.AlertDialog(heading="Error!", body="Matrix is singular and cannot be inverted.")
            dialog.add_response("ok", "OK")
            dialog.present(self)
            return
        self.matrix_data.data = inverted.tolist()
        self.matrix_view.set_matrix(self.matrix_data)
        self.matrix_view.load_matrix_values()

    def on_matrix_invert2_clicked(self, button):
        M = np.array(self.matrix_data2.data)
        try:
            inverted = np.linalg.inv(M)
        except np.linalg.LinAlgError:
            dialog = Adw.AlertDialog(heading="Error!", body="Matrix is singular and cannot be inverted.")
            dialog.add_response("ok", "OK")
            dialog.present(self)
            return
        self.matrix_data2.data = inverted.tolist()
        self.matrix_view2.set_matrix(self.matrix_data2)
        self.matrix_view2.load_matrix_values()

    def on_decomposition_changed(self, *args):
        choice = self.mode_handler.get_selected_key()   # 0 or 1 :contentReference[oaicite:1]{index=1}
        self.matrix_control_box_2.set_visible(choice == 0)
        self.action_panel_2.set_visible(choice == 0)
        self.op_dropdown_box.set_visible(choice == 0)
        self.matrix_menu_2.set_visible(choice == 0)
        self.execute_button.set_label("Calculate" if choice == 0 else "Decompose")

    # ---------- create ----------
        if choice == 0 and not hasattr(self, "matrix_view2"):
            self.matrix_view2 = MatrixView()
            self.matrix_view2.set_row_homogeneous(True)
            self.matrix_view2.set_column_homogeneous(True)
            self.matrix_view2.set_row_spacing(5)
            self.matrix_view2.set_column_spacing(5)
            self.matrix_view2.set_halign(Gtk.Align.CENTER)

            self.matrix_menu_2.insert_child_after(self.matrix_view2, self.matrix_control_box_2)

            self.rows_dropdown_2.handler_block(self._rows2_handler)
            self.cols_dropdown_2.handler_block(self._cols2_handler)
            self.rows_dropdown_2.set_selected(self.current_rows - 1)
            self.cols_dropdown_2.set_selected(self.current_cols - 1)
            self.rows_dropdown_2.handler_unblock(self._rows2_handler)
            self.cols_dropdown_2.handler_unblock(self._cols2_handler)
            self.current_rows2, self.current_cols2 = self.current_rows, self.current_cols

            self.matrix_data2 = MatrixData(self.current_rows, self.current_cols)
            self.matrix_view2.set_matrix(self.matrix_data2)

    # ---------- remove ----------
        elif choice != 0 and hasattr(self, "matrix_view2"):
            self.matrix_view2.unparent()
            del self.matrix_view2
            del self.matrix_data2

