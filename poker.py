import random
from tkinter import *

# used to load a JPG file
from PIL import ImageTk, Image

suits = ["S", "C", "D", "H"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]



class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def __str__(self):
        return "%s%s" % (self.rank, self.suit)

    def __lt__(self, other):
        return ranks.index(self.get_rank()) < ranks.index(other.get_rank())


class Deck(object):
    def __init__(self):
        self.cards = []
        for s in suits:
            for r in ranks:
                self.cards.append(Card(s, r))

    def shuffle(self):
        random.shuffle(self.cards)

    def __str__(self):
        deck = ""
        for i in range(0, 52):
            deck += str(self.cards[i]) + " "
        return deck

    def take_one(self):
        return self.cards.pop(0)


class Hand(object):
    def __init__(self, deck):
        self.cards = []
        for i in range(5):
            self.cards.append(deck.take_one())

    def __str__(self):
        hand = ""
        for i in range(5):
            hand += str(self.cards[i]) + " "
        return hand

    def is_pair(self):
        for i in range(5):
            for j in range(i+1, 5):
                if self.cards[i].get_rank() == self.cards[j].get_rank():
                    return True
        return False

    def is_two_pair(self):
        rank = None
        for i in range(5):
            for j in range(i+1, 5):
                if self.cards[i].get_rank() == self.cards[j].get_rank():
                    rank = self.cards[i].get_rank()
        if not rank:
            return False
        for i in range(5):
            if self.cards[i].get_rank() == rank:
                continue
            for j in range(i+1, 5):
                if self.cards[i].get_rank() == self.cards[j].get_rank():
                    return True
        return False

    def is_three_of_kind(self):
        for i in range(5):
            for j in range(i+1, 5):
                for k in range(j+1, 5):
                    if self.cards[i].get_rank() == self.cards[j].get_rank() and \
                       self.cards[i].get_rank() == self.cards[k].get_rank():
                        return True
        return False

    def print_canvas(self, canvas):
        size = 200, 500
        # we print the corresponding picture on the canvas list
        for i in range(5):
            card_name = self.cards[i].get_rank() + self.cards[i].get_suit() + ".jpg"
            im = Image.open("JPEG/" + card_name)
            # resize the image to fit our table
            im.thumbnail(size)
            # Put the image into a canvas compatible class, and stick in an
            # arbitrary variable to the garbage collector doesn't destroy it
            canvas[i].image = ImageTk.PhotoImage(im)
            # Add the image to the canvas, and set the anchor to the top left / north west corner
            canvas[i].create_image(20, 60, image=canvas[i].image, anchor='nw')

    def rank_hand(self):
        if self.is_three_of_kind():
            return "You have three of a kind"
        elif self.is_two_pair():
            return "You have two pairs"
        elif self.is_pair():
            return "You have a pair"
        return "You have nothing"


class GUI:
    def __init__(self, window):
        self.window = window
        bgcolor = "#20207f"
        title = "This program will deal 5 cards and tell you what hand you have got"
        window.title("Poker")
        window.geometry("1400x700")
        window.resizable(0, 0)

        self.frame = Frame(master=window, bg=bgcolor)
        self.frame.pack_propagate(0)  #Don't allow the widgets inside to determine the frame's width / height
        self.frame.pack(fill=BOTH, expand=1)  #Expand the frame to fill the root window

        # create a canvas to display the cards on
        self.cards_frame = Frame(master=self.frame)
        self.canvas = []
        for i in range(5):
            # set the background to green to simulate a table and set the border thickness to 0
            self.canvas.append(Canvas(master=self.cards_frame, width=250, height=500, bg="green", highlightthickness=0))
            self.canvas[i].grid(row=0, column=i)

        self.cards_frame.grid(row=1, padx=20)

        self.label = Label(self.frame, text="", bg=bgcolor, fg="white")
        self.label.grid(row=5)
        self.label.config(font=("Courier", 44))
        self.label2 = Label(self.frame, text=title, bg=bgcolor, fg="White")
        self.label2.grid(row=0, columnspan=2)
        self.label2.config(font=("Courier", 20))

        self.bt1 = Button(self.frame, text="Hit me!", command=self.deal)
        self.bt1.config(font=("Courier", 15))
        self.bt1.grid(row=1, column=1, columnspan=2)
        self.bt2 = Button(self.frame, text="Exit Game", command=self.exit_game, bg="black", fg="yellow")
        self.bt2.grid(row=2, column=2)

    def deal(self):
        new_deck = Deck()
        new_deck.shuffle()
        hand = Hand(new_deck)
        hand.print_canvas(self.canvas)
        self.label.config(text=hand.rank_hand())

    def exit_game(self):
        exit(0)


window = Tk(screenName="Poker")
poker_game = GUI(window)
window.mainloop()


