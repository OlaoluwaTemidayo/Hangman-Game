import tkinter as tk
import random

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Ola's Game")
        self.master.geometry("900x600")
        self.secret_word = random.choice(["python", "javascript", "java", "csharp", "ruby"])
        self.guessed_letters = []
        self.guess_count = 0
        self.max_guesses = 6
        self.hangman_parts = []
        self.initialize_gui()

    def initialize_gui(self):
        # Canvas for the hangman drawing
        self.hangman_canvas = tk.Canvas(self.master, width=300, height=300, bg="white")
        self.hangman_canvas.pack(pady=20)
        self.draw_hangman_base()

        # Label to display the word with underscores
        self.word_display = tk.Label(self.master, text="_ " * len(self.secret_word), font=("Helvetica", 30))
        self.word_display.pack(pady=(40, 10))

        # Reset button
        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game, width=20, height=2, bg="grey", fg="white")
        self.reset_button.pack(pady=10)

        # Frame for alphabet buttons
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(pady=10)

        # Label to display game status (win/lose)
        self.status_label = tk.Label(self.master, text="", font=("Helvetica", 20))
        self.status_label.pack(pady=(10, 20))

        self.setup_alphabet_buttons()

    def draw_hangman_base(self):
        # Draw the static parts of the hangman
        self.hangman_canvas.create_line(50, 250, 250, 250, width=3)  # Base
        self.hangman_canvas.create_line(150, 250, 150, 50, width=3)  # Pole
        self.hangman_canvas.create_line(150, 50, 225, 50, width=3)  # Top bar
        self.hangman_canvas.create_line(225, 50, 225, 75, width=3)  # Rope

        # Define the hangman parts to be drawn step by step
        self.hangman_parts = [
            self.hangman_canvas.create_oval(200, 75, 250, 125, width=3, state='hidden'),  # Head
            self.hangman_canvas.create_line(225, 125, 225, 175, width=3, state='hidden'),  # Body
            self.hangman_canvas.create_line(225, 135, 205, 155, width=3, state='hidden'),  # Left arm
            self.hangman_canvas.create_line(225, 135, 245, 155, width=3, state='hidden'),  # Right arm
            self.hangman_canvas.create_line(225, 175, 205, 215, width=3, state='hidden'),  # Left leg
            self.hangman_canvas.create_line(225, 175, 245, 215, width=3, state='hidden'),  # Right leg
            self.hangman_canvas.create_oval(210, 90, 240, 110, width=3, outline='black', fill='black', state='hidden'),  # Eye
            self.hangman_canvas.create_line(215, 125, 235, 125, width=3, state='hidden'),  # Mouth
        ]

    def setup_alphabet_buttons(self):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        buttons = []
        for letter in alphabet:
            button = tk.Button(self.buttons_frame, text=letter, width=4, height=2, command=lambda l=letter: self.guess_letter(l))
            buttons.append(button)
        
        # Arrange buttons in a grid
        row = 0
        col = 0
        for button in buttons:
            button.grid(row=row, column=col)
            col += 1
            if col > 8:
                col = 0
                row += 1

    def guess_letter(self, letter):
        if letter.lower() in self.secret_word and letter.lower() not in self.guessed_letters:
            self.guessed_letters.append(letter.lower())
            self.update_word_display()
            if all(letter in self.guessed_letters for letter in self.secret_word):
                self.status_label.config(text="Congratulations! You guessed it!")
                self.end_game()
        else:
            self.guess_count += 1
            self.draw_hangman_part(self.guess_count)
            if self.guess_count >= self.max_guesses:
                self.status_label.config(text=f"Game Over! The word was '{self.secret_word}'")
                self.end_game()

    def update_word_display(self):
        display_word = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.secret_word])
        self.word_display.config(text=display_word.upper())

    def draw_hangman_part(self, guess_count):
        if guess_count <= len(self.hangman_parts):
            self.hangman_canvas.itemconfigure(self.hangman_parts[guess_count-1], state='normal')

    def end_game(self):
        for child in self.buttons_frame.winfo_children():
            child.config(state=tk.DISABLED)

    def reset_game(self):
        self.guessed_letters = []
        self.guess_count = 0
        self.secret_word = random.choice(["python", "javascript", "java", "csharp", "ruby"])
        self.status_label.config(text="")
        self.word_display.config(text="_ " * len(self.secret_word))
        for child in self.buttons_frame.winfo_children():
            child.config(state=tk.NORMAL)
        for part in self.hangman_parts:
            self.hangman_canvas.itemconfigure(part, state='hidden')

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
