# Hangman (TDD + unit tests)

Features:
- Two levels: **Basic** (single word) and **Intermediate** (phrase).
- Basic single word come from a online list of words and phrases are just locally created one.
- Underscores represents hidden letters for each game round.
- 15-second timer per guess. Timeout costs one life.
- Correct guess reveals all occurrences of a letter. Incorrect guess costs one life.
- Win by revealing all letters before lives hit zero. 

## Run the game
```bash
python -m hangman.gui
```

## Run unit test
```bash
python -m unittest discover -s hangman
```

Notes:
- gui module contains the game gui interface design and timer.
- game module contains game logic like whether guess is valid or whether the play wins the game.
- selector module contains logic for game difficulty selection and generate the riddle.
