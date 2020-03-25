import random
from tkinter import *

# used to load a JPG file
from PIL import ImageTk, Image


class Game:
    def __init__(self):
        self.secret_word = 'python'
        self.proposed_word = ''
        self.counter = 0
        self.errors = 0

    def compare(self, proposed_char):
        if self.errors == 8:
            return False, 'GAME OVER!!'
        else:
            if self.secret_word == self.proposed_word:
                return "CONGRATS ! You won !"
            elif self.secret_word[self.counter] == proposed_char:
                self.proposed_word += proposed_char
                self.counter += 1
                return True, "Keep Going !"
            else:
                self.errors += 1
                return False, 'Wrong character ! {} guesses lefts'.format(8 - self.errors)

    def print_canvas(self, canvas):
        size = 200, 500
        path = "JPEG/" + str(self.errors) + ".jpg"
        #path = "JPEG/8.jpg"
        im = Image.open(path)
        im.thumbnail(size)
        canvas.image = ImageTk.PhotoImage(im)
        canvas.pimage = ImageTk.PhotoImage(im)
        canvas.create_image(200, 60, image=canvas.image, anchor='nw')
        return canvas


class GUI:
    def __init__(self, window):
        self.window = window
        bgcolor = "#20207f"
        title = "Hangman"
        window.title("Hangman")
        window.geometry("700x700")
        window.resizable(0, 0)

        self.game = Game()

        self.frame = Frame(master=window, bg=bgcolor)
        self.frame.pack_propagate(0)  # Don't allow the widgets inside to determine the frame's width / height
        self.frame.pack(fill=BOTH, expand=1)  # Expand the frame to fill the root window

        self.canvas = Canvas(master=self.frame, width=500, height=300, bg="white", highlightthickness=0)
        self.canvas.grid(row=1, padx=20)

        self.label = Label(self.frame, text="_ _ _ _ _ _", bg=bgcolor, fg="white")
        self.label.grid(row=2)
        self.label.config(font=("Courier", 44))
        self.label2 = Label(self.frame, text=title, bg=bgcolor, fg="White")
        self.label2.grid(row=0, columnspan=2)
        self.label2.config(font=("Courier", 20))
        self.label3 = Label(self.frame, text=" ", bg=bgcolor, fg="White")
        self.label3.grid(row=3, columnspan=2)
        self.label3.config(font=("Courier", 20))

        self.bt1 = Button(self.frame, text="Hit me!", command=self.deal)
        self.bt1.config(font=("Courier", 15))
        self.bt1.grid(row=5, columnspan=2)
        self.bt2 = Button(self.frame, text="Exit Game", command=self.exit_game, bg="black")
        self.bt2.grid(row=6, columnspan=2)

        self.entry_text = StringVar()  # the text in  your entry
        self.txt = Entry(self.frame, width=3, textvariable=self.entry_text)
        self.txt.grid(row=4, column=0)

    def deal(self):
        # print(self.txt.get())
        char = self.txt.get().lower()
        if len(char) == 1:
            flag, txt = self.game.compare(char)
            # print(txt)
            if flag:
                self.label3.config(text=txt, fg='green')
                _ = ['_' for i in range(len(self.game.secret_word) - len(self.game.proposed_word))]
                word_so_far = list(self.game.proposed_word) + _
                self.label.config(text=' '.join(word_so_far))
                return
            else:
                self.label3.config(text=txt, fg='red')
                self.canvas = self.game.printprint_canvas(self.canvas)
                return
        else:
            self.txt.delete(1, END)
            self.label3.config(text="Insert only 1 character !", fg='white')

    def exit_game(self):
        exit(0)


window = Tk(screenName="Hangman")
hangman = GUI(window)
window.mainloop()
