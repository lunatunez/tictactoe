# coding: utf-8
from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from field_ui import FieldUI
from playerselect import PlayerSelect
import game


class TicTacToeUI(Frame):
    def __init__(self, parent=None, _game=None):
        Frame.__init__(self, parent)
        self.ttt = _game
        TILESIZE = 50

        mainframe = ttk.Frame(parent, padding=(12, 12, 12, 12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        parent.bind('<Escape>', lambda x: self.quit())  # Quick exit

        self.symbol = _game.sym()

        self.field_vars = [StringVar() for x in range(9)]

        for i, field_var in enumerate(self.field_vars):
            #  on_click = (lambda i=i: self.btn_press(i))

            #  b = Button(mainframe, textvariable=s, font='size, 25', command=on_click)
            b = FieldUI(mainframe, size=TILESIZE, variable=field_var)
            b.bind('<Button-1>', partial(self.on_click, i))
            #  b.config(height=5, width=10)

            col, row = divmod(i, 3)
            #  buttons.pop(0).grid(row=row, column=col)
            b.grid(row=row, column=col, padx=1, pady=2)

        Label(mainframe, text="You are playing {}".format(self.ttt.PLAYERS[game.HUMAN])).grid(row=3, column=0, columnspan=3)

        # Config padding
        for child in mainframe.winfo_children():
            child.grid_configure(padx=2, pady=2, sticky='EWNS')

        self.check_cpu()

    def on_click(self, i, _event=None):
        field_var = self.field_vars[i]
        if field_var.get():
            return  # Tile has already been played on.

        result = self.ttt.b.play(i, self.ttt.sym())

        if result:
            self.field_vars[i].set(self.ttt.sym())
            #  field_var.set(next(self.symbols))
            self.assess()
            self.ttt.next_player()
            self.check_cpu()

    def set_player(self):
        if self.ttt.player == game.CPU:
            self.player.set("CPU's Turn")
        elif self.ttt.player == game.HUMAN:
            self.player.set("HUMAN's Turn")

    def check_cpu(self):
        # Check if it is the CPU's turn and run their turn.
        if self.ttt.player == game.CPU:
            cpu_move = self.ttt.cpu_turn()
            self.field_vars[cpu_move].set(self.ttt.sym())
            self.assess()
            self.ttt.next_player()

    def assess(self):
        self.ttt.check_state()
        if self.ttt.winner:
            # Change the font size of the dialog box
            self.option_add('*Dialog.msg.font', 'Helvetica 35')
            messagebox.showinfo("Game over!", self.ttt.winner)
            #  gameover = Label(self, text="Game over!k
            exit()  # Immediately exit


def run():
    root = Tk()
    root.title("TicTacToe")
    root.config(bg='black')
    root.resizable(width=False, height=False)

    # Get player selection
    inputDialog = PlayerSelect(root)
    root.wait_window(inputDialog)
    playerpick = inputDialog.selection

    tttgame = game.TicTacToe(pick=playerpick)

    TicTacToeUI(root, tttgame)

    root.mainloop()
