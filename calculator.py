"""
A tkinter GUI based Calculator
"""
import tkinter as tk


class Calculator:
    """
    A class to represent the Calculator application
    """
    all_buttons = [['C', '()', '%', '/'],
                   ['7', '8', '9', '*'],
                   ['4', '5', '6', '-'],
                   ['1', '2', '3', '+'],
                   ['<=', '0', '.', '=']]
    numeric_buttons = '0123456789'
    operator_buttons = '%/*+-'
    bracket_button = '()'
    dot = '.'
    equal_button = '='
    clear_button = 'C'
    backspace_button = '<='

    def __init__(self: object, master: object) -> object:
        """
        Constructs all necessary properties of Calculator object

        Parameters:
        - - - - - -
        master: root of the tkinter object

        """

        self.master = master
        self.master.title(' Python Calculator')
        self.master.config(bg='black')
        self.master.geometry("400x400+800+200")
        self.master.resizable(False, False)

        self.buttons = dict()
        self.last_clicked_button = None
        self.button_processed = True

        # Running expression result and history
        self.history_label = tk.Label(self.master, text='', font=('Open Sans', 10, 'normal'),
                                      bg='black', fg='gray', justify='right')
        self.history_label.grid(row=0, column=0,
                                columnspan=4,
                                pady=10, sticky='E')

        # Entry box that displays the buttons that are clicked
        self.entry_box = tk.Entry(self.master, bd=5, width=28,
                                  bg='darkgrey', font=('Open Sans', 18, 'bold'),
                                  fg='black', justify='right')
        self.entry_box.grid(row=1, column=0, rowspan=2,
                            columnspan=4, padx=10, sticky='NSEW')

        # Place all buttons on Calculator window
        for row, buttons in enumerate(Calculator.all_buttons):
            for col, btn in enumerate(buttons):
                self.buttons[btn] = tk.Button(self.master, text=btn, bd=2, width=4,
                                              bg='black', highlightcolor='dimgray',
                                              font=('Open Sans', 16, 'bold'))

                # Method that will be called on press of each button
                self.buttons[btn].config(
                    command=lambda x=btn: self.process_button(x))

                if row % 2 == 0:
                    self.buttons[btn].grid(
                        row=row + 3, column=col, padx=15, pady=15, sticky='W')
                else:
                    self.buttons[btn].grid(
                        row=row + 3, column=col, padx=15, sticky='W')

                # Colorize different types of buttons
                if btn in (Calculator.clear_button, Calculator.backspace_button):
                    self.buttons[btn].config(fg='darkorange')
                elif btn == Calculator.equal_button:
                    self.buttons[btn].config(bg='darkgreen')
                elif btn in Calculator.operator_buttons or btn == Calculator.bracket_button:
                    self.buttons[btn].config(fg='darkgreen')
                else:
                    self.buttons[btn].config(fg='ivory')

    def process_button(self: object, btn: str) -> None:
        """
        Method to process the click of Calculator button

        Parameters:
        - - - - - -
        btn: str value of the button clicked

        """
        if btn in Calculator.numeric_buttons:
            self.process_number(btn)
        elif btn in Calculator.operator_buttons:
            self.process_operator(btn)
        elif btn == Calculator.dot:
            self.process_dot()
        elif btn == Calculator.bracket_button:
            self.process_bracket()
        elif btn == Calculator.clear_button:
            self.process_clear()
        elif btn == Calculator.backspace_button:
            self.process_backspace()
        else:
            self.evaluate_entry()

        if self.button_processed:
            self.last_clicked_button = btn

    def process_number(self: object, btn: str) -> None:
        """
        Method to process the click of numerical button

        Parameters:
        - - - - - -
        btn: str value of the button clicked

        """
        self.button_processed = True

        # Number button is first button pressed
        # Append the number at end of entry box
        if self.last_clicked_button is None:
            self.entry_box.insert(0, btn)

        # Number 0 pressed when entry box has only 0, do nothing
        elif self.entry_box.get() == '0' and btn == '0':
            self.button_processed = False

        # Number pressed after equal button
        # Reset the entry box
        elif self.last_clicked_button == Calculator.equal_button:
            self.entry_box.delete(0, tk.END)
            self.entry_box.insert(0, btn)
            self.history_label.config(text='')

        # Last button was ), append * and number at the end
        elif self.entry_box.get()[-1] == Calculator.bracket_button[1]:
            self.entry_box.insert(tk.END, '*' + btn)
            self.evaluate_entry(expression=self.entry_box.get())

        # Number button pressed and entry already has operator
        # Append the number at end of entry box and evaluate the expression
        elif operator_in_string(text=self.entry_box.get()):
            self.entry_box.insert(tk.END, btn)
            self.evaluate_entry(expression=self.entry_box.get())

        # For any other case append number at end
        else:
            self.entry_box.insert(tk.END, btn)

    def process_operator(self: object, btn: str) -> None:
        """
        Method to process the click of operator button

        Parameters:
        - - - - - -
        btn: str value of the button clicked

        """
        self.button_processed = True

        # Operator is the first button pressed, do nothing
        if self.last_clicked_button is None:
            self.button_processed = False

        # Last button pressed was also an operator
        # Override old operator with current btn value
        elif self.last_clicked_button in Calculator.operator_buttons:
            self.process_backspace()
            self.entry_box.insert(tk.END, btn)
            self.button_processed = True

        # Last character on entry text in ( and current key is % or / or *
        # Do nothing
        elif self.entry_box.get()[-1] == '(' and btn in ('%', '/', '*'):
            self.button_processed = False

        # For anything else, just append the operator at end of entry text
        else:
            self.entry_box.insert(tk.END, btn)
            self.history_label.config(text='')

    def process_dot(self: object) -> None:
        """
        Method to process the click of dot button

        """

        self.button_processed = True

        # Get last position of dot
        last_dot_position = self.entry_box.get().rfind('.')

        # Dot is the first button clicked
        if self.last_clicked_button is None:
            self.entry_box.insert(0, '0.')

        # Dot clicked after operator button or (, evaluate the expression after appending 0.
        elif (self.last_clicked_button in Calculator.operator_buttons or
              self.last_clicked_button == '('):
            self.entry_box.insert(tk.END, '0.')
            self.evaluate_entry(expression=self.entry_box.get())

        # Dot clicked after ), evaluate the expression after appending *0.
        elif self.last_clicked_button == ')':
            self.entry_box.insert(tk.END, '*0.')
            self.evaluate_entry(expression=self.entry_box.get())

        # Dot clicked after equal button
        # Refresh history and initalize entry text as 0.
        elif self.last_clicked_button == Calculator.equal_button:
            self.entry_box.delete(0, tk.END)
            self.entry_box.insert(0, '0.')
            self.history_label.config(text='')

        # If last button was also dot or only numbers present since last dot position, do nothing
        elif (self.last_clicked_button == Calculator.dot or
              self.entry_box.get()[last_dot_position + 1:].isnumeric()):
            self.button_processed = False

        # Dot clicked any other time, just append at end of entry text
        else:
            self.entry_box.insert(tk.END, Calculator.dot)

    def process_bracket(self: object) -> None:
        """
        Method to process the click of () button

        """

        self.button_processed = True

        # () clicked as the first button
        if self.last_clicked_button is None:
            self.entry_box.insert(tk.END, '(')

        # () clicked and last button was number or '.' and () count matches
        # Append '*(' to entry text at end
        elif ((self.last_clicked_button in Calculator.numeric_buttons or
               self.last_clicked_button == Calculator.dot or
               self.last_clicked_button == Calculator.bracket_button) and
              self.entry_box.get().count('(') == self.entry_box.get().count(')')):
            self.entry_box.insert(tk.END, '*(')

        # () clicked and last button was number or '.' and () count dont match
        # Append ')' to entry text at end
        # evaluate the expression
        elif (self.last_clicked_button in Calculator.numeric_buttons or
              self.last_clicked_button == Calculator.dot or
              self.last_clicked_button == Calculator.bracket_button):
            self.entry_box.insert(tk.END, ')')
            self.evaluate_entry(expression=self.entry_box.get())

        # () clicked for any other case
        # Append '(' to entry text at end
        # Initialize the entry box with 0
        else:
            self.entry_box.insert(tk.END, '(')
            self.history_label.config(text='')

    def process_clear(self: object) -> None:
        """
        Method to process the click of clear button
        """
        self.button_processed = False
        self.last_clicked_button = None
        self.entry_box.delete(0, tk.END)
        self.history_label.config(text='')

    def process_backspace(self: object) -> None:
        """
        Method to process the click of backspace button
        """
        self.button_processed = False
        self.entry_box.delete(len(self.entry_box.get()) - 1, tk.END)
        self.last_clicked_button = self.entry_box.get()[-1]

    def evaluate_entry(self: object, expression: str = None) -> None:
        """
        Method to evaluate the Mathematical expression

        Parameters:
        - - - - - -
        expression: str value that denotes the series of Mathematical expressions

        """
        self.button_processed = True
        # expression is None, when equal button is clicked
        if expression is None:
            entry_text = self.entry_box.get()
            if entry_text[-1] in Calculator.operator_buttons:
                entry_text = entry_text[:-1]

            entry_text += ''.join([')' for _ in range(entry_text.count('(') -
                                                      entry_text.count(')'))])
        else:
            entry_text = expression + ''.join([')' for _ in range(expression.count('(') -
                                                                  expression.count(')'))])

        try:
            result = eval(entry_text)
        except:
            print(entry_text)
            result = 'Error'
        finally:
            if expression is None:
                self.history_label.config(text=self.entry_box.get())
                self.entry_box.delete(0, tk.END)
                self.entry_box.insert(0, result)
            else:
                self.history_label.config(text=result)


def operator_in_string(text: str) -> bool:
    """
    Returns whether input contains mathematical operators

    Parameters:
    - - - - - -
    text: string input that needs to be searched

    """
    return '%' in text or \
        '/' in text or \
        '+' in text or \
        '-' in text or \
        '*' in text


if __name__ == '__main__':
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
