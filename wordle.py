# WORDLE CLONE USING FLET
import pathlib

import flet
from flet import *

from time import sleep
import random

# control list storing rows
rows = []

# create list of valid 5-letter words
WORDLIST = pathlib.Path('words.txt')
words = [
    word.lower()
    for word in WORDLIST.read_text(encoding="utf-8").strip().split("\n")
]


# helper function with storing control instances
def storeRow(function):
    def wrapper(*args, **kwargs):
        res = function(*args, **kwargs)
        rows.append(res)
        return res

    return wrapper

# class to display errors
class GameErrorHandler(UserControl):
    def __init__(self):
        super().__init__()

    @storeRow
    def set_error_text(self):
        return Text(size=11, weight="bold")

    def build(self):
        return Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                self.set_error_text()
            ]
        )

# class to control game input guesses and game logic
class GameInput(UserControl):
    def __init__(self, word: str):
        self.line = 0 # keeps track of rows
        self.guess = 5 # number of guesses
        self.word = word
        super().__init__()

    # game logic
    def get_letters(self, e):
        # submitted word variables
        word, is_word = e.control.value, e.control.value

        # check if word is 5-letters long
        if len(word) == 5:
            # check if word is a valid english word
            if word in words:
                word = [*word]

                # check if word submitted is correct word
                if is_word == self.word:
                    # display game stats
                    rows[6].value = f"CORRECT! THE WORD IS: {self.word.upper()}"
                    rows[6].update()

                elif self.line > 5 or self.guess < 1:
                    rows[6].value = f"NO MORE GUESSES REMAINING! THE WORD WAS: {self.word.upper()}. TRY AGAIN."
                    rows[6].update()

                for index, box in enumerate(rows[self.line].controls[:]):
                    if word[index] in self.word:
                        # letter in word at this position. change color to green
                        if word[index] == self.word[index]:
                            box.content.value = word[index].upper()
                            box.content.offset = transform.Offset(0, 0)
                            box.content.opacity = 1
                            box.bgcolor = "green900"
                            box.update()
                            sleep(0.4)

                        # letter in word but in the wrong position. change color to yellow
                        else:
                            box.content.value = word[index].upper()
                            box.content.offset = transform.Offset(0, 0)
                            box.content.opacity = 1
                            box.bgcolor = "#b59e38" # yellow
                            box.update()
                            sleep(0.4)

                    # letter no in the word so remain color
                    else:
                        box.content.value = word[index].upper()
                        box.content.offset = transform.Offset(0, 0)
                        box.content.opacity = 1
                        box.update()
                        sleep(0.4)

                # update line and guess variables
                self.line += 1
                self.guess -= 1

            # submit errors
            else:
                rows[6].value = f"NOT A WORD! TRY AGAIN!"
                rows[6].update()

        else:
            rows[6].value = f"WORD MUST BE 5 LETTERS! TRY AGAIN!"
            rows[6].update()

        # clear entry
        e.control.value = ""
        e.control.update()

    #
    def clear_error(self, e):
        rows[6].value = ""
        rows[6].update()

    # textfield UI
    def build(self):
        return Row(
            spacing=20,
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Container(
                    height=45,
                    width=250,
                    border=border.all(0.5, colors.WHITE24),
                    border_radius=6,
                    content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            TextField(
                                border_color="transparent",
                                bgcolor="transparent",
                                height=20,
                                width=200,
                                text_size=12,
                                content_padding=3,
                                cursor_color="white",
                                cursor_width=1,
                                color="white",
                                hint_text="Type a 5-letter word...",
                                text_align="center",
                                on_submit=lambda e: self.get_letters(e),
                                on_focus=lambda e: self.clear_error(e),
                            ),
                        ],
                    ),
                )
            ],
        )

class GameGrid(UserControl):
    def __init__(self):
        super().__init__()

    @storeRow
    def createSingleRow(self):
        row = Row(alignment=MainAxisAlignment.CENTER)
        for __ in range(5):
            row.controls.append(
                Container(
                    width=52,
                    height=52,
                    border=border.all(0.5, colors.WHITE24),
                    alignment=alignment.center,
                    clip_behavior=ClipBehavior.HARD_EDGE,
                    animate=animation.Animation(300, "decelerate"),
                    content=Text(
                        size=20,
                        weight="bold",
                        opacity=0,
                        offset=transform.Offset(0, 0.75),
                        animate_opacity=animation.Animation(400, "decelerate"),
                        animate_offset=animation.Animation(400, "decelerate"),
                    ),
                )
            )

        return row

    def build(self):
        return Column(
            controls=[
                self.createSingleRow(),
                self.createSingleRow(),
                self.createSingleRow(),
                self.createSingleRow(),
                self.createSingleRow(),
                self.createSingleRow(),
            ]
        )

# main game function
def main(page: Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # generate random word from list
    word = random.choice(words)

    # main UI
    page.add(
        Column(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[Text("WORDLE", size=25, weight="bold")],
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[Text("Wordle Clone by James Choi", size=12, weight="bold", color=colors.WHITE54)]
                ),
                Divider(height=20, color=colors.TRANSPARENT),
                GameGrid(),
                Divider(height=10, color=colors.TRANSPARENT),
                GameInput(word),
                Divider(height=10, color=colors.TRANSPARENT),
                GameErrorHandler()
            ]
        )
    )

    page.update()

if __name__ == "__main__":
    flet.app(target=main)






