"""A simple GUI for the Hangman game using Tkinter."""

import tkinter as tk
from tkinter import messagebox
from hangman.game import HangmanGame, GuessResult   # pylint: disable= [E0401]
from hangman.selector import Level, WordSelector  # pylint: disable= [E0401]


# pylint: disable=too-many-instance-attributes
class HangmanGUI:
    """Main class for Hangman GUI application."""
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman (GUI)")
        self.root.geometry("600x450")

        # Level selection area
        self.level_var = tk.StringVar(value="Basic")
        tk.Label(root, text="Select Level:").pack(pady=5)
        tk.Radiobutton(root, text="Basic", variable=self.level_var, value="Basic").pack()    # noqa: E501 pylint: disable= [C0301]
        tk.Radiobutton(root, text="Intermediate", variable=self.level_var, value="Intermediate").pack()  # noqa: E501 pylint: disable= [C0301]

        self.start_btn = tk.Button(root, text="Start Game", command=self.start_game)  # noqa: E501
        self.start_btn.pack(pady=10)

        # Game area
        self.word_label = tk.Label(root, text="", font=("Courier", 24))
        self.word_label.pack(pady=20)

        self.lives_label = tk.Label(root, text="", font=("Arial", 14))
        self.lives_label.pack()

        self.timer_label = tk.Label(root, text="", font=("Arial", 14), fg="red")  # noqa: E501
        self.timer_label.pack(pady=5)

        self.guess_entry = tk.Entry(root, font=("Arial", 14))
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda e: self.make_guess())

        self.guess_btn = tk.Button(root, text="Guess", command=self.make_guess)
        self.guess_btn.pack()

        self.guessed_label = tk.Label(root, text="", font=("Arial", 12))
        self.guessed_label.pack(pady=10)

        self.timer_job = None
        self.remaining_time = 0
        self.game = None
        self.reset_game()

    def update_display(self):
        """Update the GUI display based on current game state."""
        self.word_label.config(text=self.game.masked())
        self.lives_label.config(text=f"Lives: {self.game.lives}")
        guessed = ", ".join(sorted(self.game.guessed)) if self.game.guessed else "_"  # noqa: E501
        self.guessed_label.config(text=f"Guessed: {guessed}")

    def start_game(self):
        """Initialize and start a new game."""
        if self.level_var.get() == "Basic":
            level = Level.BASIC
        else:
            level = Level.INTERMEDIATE
        selector = WordSelector()
        self.game = HangmanGame(selector, level, max_lives=6)
        self.update_display()
        self.start_timer()
        self.start_btn.config(state=tk.DISABLED)

    def reset_game(self):
        """Reset game-related variables."""
        self.game = None
        self.remaining_time = 0
        self.timer_job = None
        self.start_btn.config(state=tk.NORMAL)

    # ---------------- Timer handling ----------------
    def start_timer(self):
        """Start or restart the countdown timer and update the display"""
        self.remaining_time = 15
        self.update_timer()

    def update_timer(self):
        """Update the timer display every second."""
        self.timer_label.config(text=f"Time left: {self.remaining_time}s")
        if self.remaining_time <= 0:
            self.time_expired()
            return
        self.remaining_time -= 1
        self.timer_job = self.root.after(1000, self.update_timer)

    def time_expired(self):
        """When time is up, lose one life and continue."""
        if not self.game:
            return
        self.game.time_out()
        messagebox.showwarning("Time's up!", "Lost 1 life.")
        self.update_display()
        self.check_endgame()
        if self.game:  # continue if not ended
            self.start_timer()

    def reset_timer(self):
        """Reset the timer for the next guess."""
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
        self.start_timer()

    # ---------------- Guess handling ----------------
    def make_guess(self):
        """Process the player's guess."""
        guess = self.guess_entry.get().strip().lower()
        self.guess_entry.delete(0, tk.END)
        if not guess:
            return

        result = self.game.guess_letter(guess[0])
        if result == GuessResult.INVALID:
            messagebox.showinfo("Invalid", "Enter a single alphabetic letter.")
        elif result == GuessResult.REPEATED:
            messagebox.showinfo("Repeated", f"You already guessed '{guess[0]}'.")  # noqa: E501

        self.update_display()
        self.check_endgame()
        if self.game:  # restart timer for next turn
            self.reset_timer()

    # ---------------- Endgame ----------------
    def check_endgame(self):
        """Check if the game needs to be ended."""
        if self.game.is_won():
            if self.timer_job:  # Cancel the timer if it's running
                self.root.after_cancel(self.timer_job)
            messagebox.showinfo("Victory!", f"You found it! The answer was: {self.game.answer}")  # noqa: E501 pylint: disable= [C0301]
            self.reset_game()
        elif self.game.is_lost():
            if self.timer_job:  # Cancel the timer if it's running
                self.root.after_cancel(self.timer_job)
            messagebox.showerror("Game Over", f"Out of lives! The answer was: {self.game.answer}")  # noqa: E501 pylint: disable= [C0301]
            self.reset_game()


def main():
    """Run the Hangman GUI application."""
    root = tk.Tk()
    HangmanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
