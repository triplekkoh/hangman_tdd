"""Unit tests for the Hangman game."""

# flake8: noqa: E501

import unittest
import tkinter as tk
from hangman.gui import HangmanGUI
from hangman.game import HangmanGame, GuessResult
from hangman.selector import WordSelector, Level, BASIC_WORDS


class DummySelector(WordSelector):
    """A dummy word selector for testing with a fixed word."""
    def __init__(self, word):
        self.word = word
        super().__init__(word)

    def pick_a_word(self, level):
        return self.word

class TestHangmanGame(unittest.TestCase):
    """Unit tests for Hangman game logic and GUI."""
    #Test section 1 for word selection and Level enum.
    def test_check_default_level(self):
        """Test Level default values."""
        selector = WordSelector()
        self.assertEqual(selector.level.name, "BASIC")

    def test_check_change_inter(self):
        """Test changing Level values to intermediate."""
        selector = WordSelector(level=Level.INTERMEDIATE)
        self.assertEqual(selector.level.name, "INTERMEDIATE")

    def test_level_change_basic(self):
        """Test changing Level values back to Basic."""
        selector = WordSelector(level=Level.INTERMEDIATE)
        selector.level = Level.BASIC
        self.assertEqual(selector.level.name, "BASIC")

    def test_basic_pick_word(self):
        """Test whether can pick a word from Basic level from word_link."""
        selector = WordSelector(level=Level.BASIC)
        word = selector.pick_a_word(Level.BASIC)
        self.assertIsInstance(word, str)
        self.assertTrue(len(word) > 0)
        print(f"test_basic_pick_word: Basic level word picked: {word}")

    def test_basic_pick_word_different(self):
        """Test whether can pick different words from word_link."""
        selector = WordSelector(level=Level.BASIC)
        word1 = selector.pick_a_word(Level.BASIC)
        word2 = selector.pick_a_word(Level.BASIC)
        self.assertIsInstance(word1, str)
        self.assertIsInstance(word2, str)
        self.assertNotEqual(word1, word2)
        print(f"test_basic_pick_word_different: Words picked: {word1}, {word2}")

    def test_inter_pick_phrase(self):
        """Test whether can pick a phrase from Intermediate level."""
        selector = WordSelector(level=Level.INTERMEDIATE)
        phrase = selector.pick_a_word(Level.INTERMEDIATE)
        self.assertIsInstance(phrase, str)
        print(f"test_inter_pick_phrase: Intermediate level phrase picked: {phrase}")

    def test_inter_pick_phrase_different(self):
        """Test whether can pick different phrases from Intermediate level."""
        selector = WordSelector(level=Level.INTERMEDIATE)
        phrase1 = selector.pick_a_word(Level.INTERMEDIATE)
        phrase2 = selector.pick_a_word(Level.INTERMEDIATE)
        self.assertIsInstance(phrase1, str)
        self.assertIsInstance(phrase2, str)
        self.assertNotEqual(phrase1, phrase2)
        print(f"test_inter_pick_phrase_different: Phrases picked: {phrase1}, {phrase2}")

    def test_invalid_level(self):
        """Test that invalid level raises ValueError."""
        selector = WordSelector()
        with self.assertRaises(ValueError):
            selector.pick_a_word("ANYLEVEL")

    # Test section 2 for hangman game logic.
    def test_default_game_state(self):
        """Test initial game state."""
        selector = WordSelector(level=Level.BASIC)
        game = HangmanGame(selector, level=Level.BASIC)
        self.assertEqual(game.level.name, "BASIC")
        self.assertEqual(game.max_lives, 6)
        self.assertEqual(game.lives, game.max_lives)
        self.assertIn(game.answer, [word.decode('UTF-8') for word in BASIC_WORDS])

    def test_masked_initial(self):
        """Test masked function returns underscores for unguessed letters."""
        selector = DummySelector("banana")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        self.assertEqual(game.masked(), "______")

    def test_masked_after_some_guesses(self):
        """Test masked function after some correct guesses."""
        selector = DummySelector("banana")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        game.guessed.add("a")
        game.guessed.add("b")
        self.assertEqual(game.masked(), "ba_a_a")

    def test_valid_guess(self):
        """Test valid_guess function."""
        selector = DummySelector("apple")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        self.assertTrue(game.valid_guess("a"))
        self.assertFalse(game.valid_guess("1"))
        self.assertFalse(game.valid_guess("abc"))
        self.assertFalse(game.valid_guess(""))
        self.assertFalse(game.valid_guess("@"))

    def test_guess_letter_correct(self):
        """Test guess_letter returns CORRECT for a correct guess."""
        selector = DummySelector("apple")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        result = game.guess_letter("a")
        self.assertEqual(result, GuessResult.CORRECT)
        self.assertIn("a", game.guessed)
        self.assertEqual(game.masked(), "a____")

    def test_guess_letter_incorrect(self):
        """Test guess_letter returns INCORRECT for a wrong guess and a live deducted."""
        selector = DummySelector("apple")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        result = game.guess_letter("z")
        self.assertEqual(result, GuessResult.INCORRECT)
        self.assertIn("z", game.guessed)
        self.assertEqual(game.masked(), "_____")
        self.assertEqual(game.lives, game.max_lives - 1)

    def test_guess_letter_repeated(self):
        """Test guess_letter returns REPEATED for a repeated guess."""
        selector = DummySelector("apple")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        game.guess_letter("a")
        result = game.guess_letter("a")
        self.assertEqual(result, GuessResult.REPEATED)

    def test_guess_letter_invalid(self):
        """Test guess_letter returns INVALID for invalid input."""
        selector = DummySelector("cake")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        result = game.guess_letter("1")
        self.assertEqual(result, GuessResult.INVALID)
        result = game.guess_letter("")
        self.assertEqual(result, GuessResult.INVALID)
        result = game.guess_letter("ab")
        self.assertEqual(result, GuessResult.INVALID)
        result = game.guess_letter("&")
        self.assertEqual(result, GuessResult.INVALID)

    def test_guess_letter_case_insensitivity(self):
        """Test guess_letter is case-insensitive."""
        selector = DummySelector("Apple")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        result_lower = game.guess_letter("a")
        result_upper = game.guess_letter("P")
        self.assertEqual(result_lower, GuessResult.CORRECT)
        self.assertEqual(result_upper, GuessResult.CORRECT)
        self.assertIn("a", game.guessed)
        self.assertIn("p", game.guessed)
        self.assertEqual(game.masked(), "app__")

    def test_masked_all_letters_guessed(self):
        """Test masked function when all letters are guessed."""
        selector = DummySelector("dog")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        for ch in "dog":
            game.guess_letter(ch)
        self.assertEqual(game.masked(), "dog")

    def test_masked_with_repeated_letters(self):
        """Test masked function with repeated letters in answer."""
        selector = DummySelector("letter")
        game = HangmanGame(selector=selector, level=Level.BASIC, max_lives=5)
        game.guess_letter("e")
        self.assertEqual(game.masked(), "_e__e_")
        game.guess_letter("t")
        self.assertEqual(game.masked(), "_ette_")

    def test_is_won_true(self):
        """Test is_won returns True when all letters are guessed."""
        selector = DummySelector("cat")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        for ch in "cat":
            game.guess_letter(ch)
        self.assertTrue(game.is_won())

    def test_is_won_false(self):
        """Test is_won returns False when not all letters are guessed."""
        selector = DummySelector("cat")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        game.guess_letter("c")
        game.guess_letter("a")
        self.assertFalse(game.is_won())

    def test_is_lost_true(self):
        """Test is_lost returns True when lives reach zero and not won."""
        selector = DummySelector("bat")
        game = HangmanGame(selector=selector, level=Level.BASIC, max_lives=3)
        game.guess_letter("x")
        game.guess_letter("y")
        game.guess_letter("z")
        self.assertTrue(game.is_lost())

    def test_is_lost_false(self):
        """Test is_lost returns False when lives remain or game is won."""
        selector = DummySelector("bat")
        game = HangmanGame(selector=selector, level=Level.BASIC, max_lives=3)
        game.guess_letter("x")
        game.guess_letter("b")
        self.assertFalse(game.is_lost())
        game.guess_letter("a")
        game.guess_letter("t")
        self.assertFalse(game.is_lost())
        self.assertTrue(game.is_won())

    def test_time_out_deducts_life(self):
        """Test time_out deducts one life."""
        selector = DummySelector("fish")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        initial_lives = game.lives
        game.time_out()
        self.assertEqual(game.lives, initial_lives - 1)

    def test_gui_setup(self):
        """Set up a GUI instance with a dummy game for testing."""
        root = tk.Tk()
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui = HangmanGUI(root)
        self.assertIsNotNone(gui)
        gui.game = game
        root.destroy()
        self.assertIs(gui.game, game)

    def test_update_display(self):
        """Test that the GUI display updates correctly."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.update_display()
        self.assertEqual(gui.lives_label.cget("text"), "Lives: 6")
        self.assertEqual(gui.guessed_label.cget("text"), "Guessed: _")
        root.destroy()

    def test_start_game(self):
        """Test that the GUI starts the game correctly."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        self.assertEqual(gui.game.lives, 6)
        self.assertNotEqual(gui.remaining_time, 0)
        self.assertEqual(gui.start_btn.config('state')[-1], tk.DISABLED)
        root.destroy()

    def test_reset_game(self):
        """Test that the GUI resets the game correctly."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        self.assertEqual(gui.game.lives, 6)
        self.assertNotEqual(gui.remaining_time, 0)
        self.assertEqual(gui.start_btn.config('state')[-1], tk.DISABLED)
        gui.reset_game()
        self.assertEqual(gui.remaining_time, 0)
        self.assertEqual(gui.start_btn.config('state')[-1], tk.NORMAL)
        root.destroy()

    def test_update_timer(self):
        """Test that the timer updates correctly."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.update_timer()
        self.assertLess(gui.remaining_time, 15)
        root.destroy()

    def test_timer_expired(self):
        """Test that the timer expiration is handled correctly."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.remaining_time = 0
        gui.update_timer()
        self.assertLess(gui.game.lives, 6)
        root.destroy()

    def test_reset_timer(self):
        """Test that the timer resets correctly."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.remaining_time = 0
        gui.reset_timer()
        self.assertEqual(gui.remaining_time, 14)
        root.destroy()

    def test_make_guess(self):
        """Test that making a guess updates the game state."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.guess_entry.insert(0, "p")
        gui.make_guess()
        self.assertIn("p", gui.game.guessed)
        root.destroy()

    def test_make_repeated_guess(self):
        """Test that making a repeated guess is handled correctly."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.guess_entry.insert(0, "p")
        gui.make_guess()
        self.assertIn("p", gui.game.guessed)
        gui.guess_entry.insert(0, "p")
        gui.make_guess()
        root.destroy()

    def test_make_invalid_guess(self):
        """Test that making an invalid guess is handled correctly."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.guess_entry.insert(0, "1")
        gui.make_guess()
        self.assertNotIn("1", gui.game.guessed)
        root.destroy()

    def test_timer_reset_after_guess(self):
        """Test that the timer resets after a valid guess."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("python")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.guess_entry.insert(0, "p")
        gui.make_guess()
        self.assertEqual(gui.remaining_time, 14)
        root.destroy()
        
    def test_check_endgame_win(self):
        """Test that the endgame is detected correctly on win."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("go")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.game.guessed = gui.game.answer
        self.assertTrue(gui.game.is_won())
        root.destroy()

    def test_check_endgame_loss(self):
        """Test that the endgame is detected correctly on loss."""
        root = tk.Tk()
        gui = HangmanGUI(root)
        selector = DummySelector("go")
        game = HangmanGame(selector=selector, level=Level.BASIC)
        gui.game = game
        gui.start_game()
        gui.game.lives = 0
        self.assertTrue(gui.game.is_lost())
        root.destroy()

if __name__ == "__main__":
    unittest.main()
