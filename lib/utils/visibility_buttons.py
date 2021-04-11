class VisibilityButtons:
    """
    Object that keeps track of which button should be shown on NeuralEditPage
    """

    def __init__(self, values):
        self.values = values
        self.buttons = []
        self.positions = []

    def add_button(self, button, pos):
        self.buttons.append(button)
        self.positions.append(pos)

    def __setitem__(self, index, value):
        self.values[index] = value
        button = self.buttons[index]
        
        if not value:
            button["widget"].grid_forget()
        else:
            pos = self.positions[index]
            button["widget"].grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])

    def show_next(self):
        for i in range(len(self.values)):
            if i == 0:
                continue

            if not self.values[i]:
                self.__setitem__(i, True)
                return i
                break

    def hide_last_visible(self):
        for i in range(len(self.values)):
            if i == 0:
                continue

            if not self.values[i]:
                self.__setitem__(i-1, False)
                break