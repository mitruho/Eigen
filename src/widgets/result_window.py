import numpy as np
from gi.repository import Gtk, Adw, Gdk


def _format_scalar(val):
    if np.iscomplex(val) and val.imag != 0:
        sign = "+" if val.imag >= 0 else "-"
        return f"{val.real:.4g} {sign} {abs(val.imag):.4g}i"
    return f"{val.real:.4g}"

def _format_vector(vec):
    return "[" + ",  ".join(_format_scalar(v) for v in vec) + "]"

def _format_matrix(mat):
    rows = [
        "[" + ",  ".join(_format_scalar(mat[r, c]) for c in range(mat.shape[1])) + "]"
        for r in range(mat.shape[0])
    ]
    return "[" + ",\n ".join(rows) + "]"

def _copy_to_clipboard(text):
    Gdk.Display.get_default().get_clipboard().set_content(
        Gdk.ContentProvider.new_for_value(text)
    )

def _make_copy_button(text):
    btn = Gtk.Button()
    btn.set_icon_name("edit-copy-symbolic")
    btn.add_css_class("flat")
    btn.set_valign(Gtk.Align.CENTER)
    btn.connect("clicked", lambda _, t=text: _copy_to_clipboard(t))
    return btn


class ResultWindow(Adw.Dialog):
    """Dialog that displays eigenvalue decomposition results."""

    def __init__(self, eigenvalues, eigenvectors):
        super().__init__()
        self.set_title("Decomposition Result")
        self.set_content_width(420)
        self.set_content_height(400)

        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors

        toolbar_view = Adw.ToolbarView()
        self.set_child(toolbar_view)
        toolbar_view.add_top_bar(Adw.HeaderBar())

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
            text = _format_scalar(val)
            row = Adw.ActionRow()
            row.set_title(f"\u03bb{i + 1}")
            row.set_subtitle(text)
            row.add_suffix(_make_copy_button(text))
            ev_group.add(row)

        copy_ev_btn = Gtk.Button(label="Copy as vector")
        copy_ev_btn.add_css_class("pill")
        copy_ev_btn.set_halign(Gtk.Align.END)
        copy_ev_btn.connect("clicked", lambda _: _copy_to_clipboard(_format_vector(eigenvalues)))
        box.append(copy_ev_btn)

        # Eigenvectors section
        evec_group = Adw.PreferencesGroup()
        evec_group.set_title("Eigenvectors")
        box.append(evec_group)

        for i in range(eigenvectors.shape[1]):
            col = eigenvectors[:, i]
            text = _format_vector(col)
            row = Adw.ActionRow()
            row.set_title(f"v{i + 1}")
            row.set_subtitle(text)
            row.add_suffix(_make_copy_button(text))
            evec_group.add(row)

        copy_evec_btn = Gtk.Button(label="Copy as matrix")
        copy_evec_btn.add_css_class("pill")
        copy_evec_btn.set_halign(Gtk.Align.END)
        copy_evec_btn.connect("clicked", lambda _: _copy_to_clipboard(_format_matrix(eigenvectors)))
        box.append(copy_evec_btn)


class CalcResultDialog(Adw.Dialog):
    """Dialog that displays the result of a matrix arithmetic operation."""

    def __init__(self, result):
        super().__init__()
        self.set_title("Result")
        self.set_content_width(420)
        self.set_content_height(350)

        self._result = result

        toolbar_view = Adw.ToolbarView()
        self.set_child(toolbar_view)
        toolbar_view.add_top_bar(Adw.HeaderBar())

        scroll = Gtk.ScrolledWindow()
        scroll.set_propagate_natural_height(True)
        toolbar_view.set_content(scroll)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(18)
        box.set_margin_bottom(18)
        box.set_margin_start(18)
        box.set_margin_end(18)
        scroll.set_child(box)

        group = Adw.PreferencesGroup()
        group.set_title("Result Matrix")
        box.append(group)

        for r in range(result.shape[0]):
            text = _format_vector(result[r])
            row = Adw.ActionRow()
            row.set_title(f"Row {r + 1}")
            row.set_subtitle(text)
            row.add_suffix(_make_copy_button(text))
            group.add(row)

        copy_btn = Gtk.Button(label="Copy as matrix")
        copy_btn.add_css_class("pill")
        copy_btn.set_halign(Gtk.Align.END)
        copy_btn.connect("clicked", lambda _: _copy_to_clipboard(_format_matrix(result)))
        box.append(copy_btn)
