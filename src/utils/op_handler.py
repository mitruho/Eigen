from gi.repository import Gtk

class OpHandler:
    def __init__(self, dropdown, selected=0):
        """
        Initializes the OpHandler for managing matrix operations in calculator mod.

        Args:
            *dropdown (Gtk.DropDown): The dropdown widget.
            selected (int, optional): The default selected index. Defaults to 0.
        """
        self.dropdown = dropdown
        self.selected = selected
        self._setup_dropdowns()

    def _setup_dropdowns(self):
        """
        Sets up the dropdown for matrix operations.
        """
        options = ["+", "−", "·"]
        model = Gtk.StringList.new(options)

        # for dropdown in self.dropdowns:
        self.dropdown.set_model(model)
        self.dropdown.set_selected(self.selected)

    def get_selected_op(self):
        """
        Returns a selected values from dropdown.

        Returns:
            str: The selected value
        """
        op = self.dropdown.get_selected()
        return op
    

