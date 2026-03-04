import numpy as np
from gi.repository import Gtk, Adw, Gdk


class ResultWindow(Adw.Dialog):
    """
    A dialog that displays eigenvalue decomposition results.

    Shows eigenvalues and their corresponding eigenvectors
    computed from the input matrix.
    """

    def __init__(self, eigenvalues, eigenvectors):
        """
        Initializes the ResultWindow.

        Args:
            eigenvalues (np.ndarray): 1-D array of eigenvalues.
            eigenvectors (np.ndarray): 2-D array whose columns are eigenvectors.
        """
        super().__init__()
        self.set_title("Decomposition Result")
        self.set_content_width(420)
        self.set_content_height(400)

        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors

        toolbar_view = Adw.ToolbarView()
        self.set_child(toolbar_view)

        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)

        scroll = Gtk.ScrolledWindow()
        scroll.set_propagate_natural_height(True)
        toolbar_view.set_content(scroll)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(18)
        box.set_margin_bottom(18)
        box.set_margin_start(18)
        box.set_margin_end(18)
        scroll.set_child(box)

        # Eigenvalues section
        ev_group = Adw.PreferencesGroup()
        ev_group.set_title("Eigenvalues")
        box.append(ev_group)

        for i, val in enumerate(eigenvalues):
            text = self._format_scalar(val)
            row = Adw.ActionRow()
            row.set_title(f"\u03bb{i + 1}")
            row.set_subtitle(text)
            row.add_suffix(self._make_copy_button(text))
            ev_group.add(row)

        copy_ev_btn = Gtk.Button(label="Copy as vector")
        copy_ev_btn.add_css_class("pill")
        copy_ev_btn.set_halign(Gtk.Align.END)
        copy_ev_btn.connect(
            "clicked",
            lambda _: self._copy_to_clipboard(self._format_vector(eigenvalues)),
        )
        box.append(copy_ev_btn)

        # Eigenvectors section
        evec_group = Adw.PreferencesGroup()
        evec_group.set_title("Eigenvectors")
        box.append(evec_group)

        for i in range(eigenvectors.shape[1]):
            col = eigenvectors[:, i]
            text = self._format_vector(col)
            row = Adw.ActionRow()
            row.set_title(f"v{i + 1}")
            row.set_subtitle(text)
            row.add_suffix(self._make_copy_button(text))
            evec_group.add(row)

        copy_evec_btn = Gtk.Button(label="Copy as matrix")
        copy_evec_btn.add_css_class("pill")
        copy_evec_btn.set_halign(Gtk.Align.END)
        copy_evec_btn.connect(
            "clicked",
            lambda _: self._copy_to_clipboard(self._format_matrix(eigenvectors)),
        )
        box.append(copy_evec_btn)

    def _make_copy_button(self, text):
        btn = Gtk.Button()
        btn.set_icon_name("edit-copy-symbolic")
        btn.add_css_class("flat")
        btn.set_valign(Gtk.Align.CENTER)
        btn.connect("clicked", lambda _, t=text: self._copy_to_clipboard(t))
        return btn

    def _copy_to_clipboard(self, text):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set_content(Gdk.ContentProvider.new_for_value(text))

    def _format_scalar(self, val):
        """Format a potentially complex scalar for display."""
        if np.iscomplex(val) and val.imag != 0:
            sign = "+" if val.imag >= 0 else "-"
            return f"{val.real:.4g} {sign} {abs(val.imag):.4g}i"
        return f"{val.real:.4g}"

    def _format_vector(self, vec):
        """Format a 1-D array as a bracketed list."""
        return "[" + ",  ".join(self._format_scalar(v) for v in vec) + "]"

    def _format_matrix(self, mat):
        """Format a 2-D array as a bracketed row-major matrix string."""
        rows = [
            "[" + ",  ".join(self._format_scalar(mat[r, c]) for c in range(mat.shape[1])) + "]"
            for r in range(mat.shape[0])
        ]
        return "[" + ",\n ".join(rows) + "]"
