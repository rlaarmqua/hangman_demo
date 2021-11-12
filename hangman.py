import random
import os
from enum import Enum, auto
import math

#https://www.delftstack.com/de/howto/python/python-clear-console/
def clearConsole():
    command = 'clear' if os.name not in ('nt', 'dos') else 'cls'  # If Machine is running on Windows, use cls
    os.system(command)


class State(Enum):
    START = auto(),
    START_NEXT_ROUND = auto(),
    PRINT_RULES = auto(),
    PLAY_TURN = auto(),
    CHECK_SOLUTION = auto(),
    ASK_PLAY_AGAIN = auto(),
    END = auto(),


class Hangman():
    possible_words = ["Hund", "Waschmaschine", "Quietscheente"]
    WRONG_GUESS_PENALTY = 1
    WRONG_SOLUTION_PENALTY = 3
    CORRECT_SOLUTION_BONUS = -5

    def __init__(self, num_players=2):
        self.num_players = num_players
        self.state = State.START

        self.errors = [0 for _ in range(num_players)]
        self.active_player = random.choice(list(range(self.num_players)))
        self.word = random.choice(Hangman.possible_words).lower()
        self.identified_letters = set()
        self.wrong_letters = set()

    def run(self):
        while self.state != State.END:
            if self.state == State.START:
                print("Hallo! Willkommen bei Hangman! Möchtest du erst die Regeln erfahren? (ja/nein)")
                response = input('>')
                if response.lower() == 'ja':
                    self.state = State.PRINT_RULES
                else:
                    self.state = State.START_NEXT_ROUND
                continue

            if self.state == State.PRINT_RULES:
                self.explain_rules()
                self.state = State.PLAY_TURN
                continue

            if self.state == State.START_NEXT_ROUND:
                self.prepare_round()
                self.state = State.PLAY_TURN
                continue

            if self.state == State.PLAY_TURN:
                self.print_current_game_state()
                response = self.ask_for_letter()
                self.state = self.evaluate_answer(response)
                continue

            if self.state == State.CHECK_SOLUTION:
                solution = self.request_solution()
                self.state = self.check_solution(solution)
                continue

            if self.state == State.ASK_PLAY_AGAIN:
                self.state = self.ask_to_play_again()
                continue

            if self.state == State.END:
                self.announce_winners()
                print("Okay! Bye-bye!")

    def next_player(self):
        self.active_player = (self.active_player + 1) % self.num_players

    def prepare_round(self):
        self.next_player()
        self.word = random.choice(Hangman.possible_words).lower()
        self.identified_letters = set()
        self.wrong_letters = set()

    def explain_rules(self):
        clearConsole()
        print("Das Spiel funktioniert so: Es gibt zwei Spieler und den Computer.\n"
              "Der Computer denkt sich ein Wort aus und die Spieler müssen es erraten.\n"
              "Wenn ein Spieler am Zug ist, darf er einen Buchstaben raten.\n"
              "Wenn der Buchstabe im Wort enthalten ist, darf der Spieler nochmal raten, \n"
              "ansonsten ist der andere Spieler an der Reihe.\n"
              "Für jeden falsch geratenen Buchstaben gibt es 1 Strafpunkt.\n"
              "Wenn ihr das Wort lösen möchtet, schreibt 'lösen'.\n"
              "Wenn ihr die Regeln nochmal lesen möchtet, schreibt 'Regeln'.\n"
              "Achtung! Bei falscher Lösung gibt es 3 Strafpunkte! "
              "Wer das Wort rät, bekommt 5 Strafpunkte abgezogen."
              "Wer am Ende die wenigsten Strafpunkte hat, gewinnt! , gewinnt! Viel Spaß :)")

    def print_current_game_state(self):
        print("Welches Wort wird gesucht?")
        output = [l if l in self.identified_letters else "_" for l in self.word]
        print(" ".join(output))
        for player in range(self.num_players):
            print(f"Spieler{player + 1}: ", self.errors[player], " Strafpunkt(e)")
        print()

    def ask_for_letter(self):
        print(f"Spieler{self.active_player + 1} ist an der Reihe!")
        print("Welchen Buchstaben rätst du?")
        return input(">").upper()

    def evaluate_answer(self, guessed_letter):
        guessed_letter = guessed_letter.lower()
        if len(guessed_letter) != 1:
            if guessed_letter == "lösen":
                return State.CHECK_SOLUTION

            if guessed_letter == "regeln":
                return State.PRINT_RULES

            clearConsole()
            print("Was war das? Wenn du lösen möchtest, schreib bitte 'lösen'! "
                  "Ansonsten verstehe ich nur einzelne Buchstaben :)")
            return State.PLAY_TURN

        clearConsole()
        if guessed_letter in self.word:
            print("Gut geraten!")
            self.identified_letters.add(guessed_letter.lower())
        else:
            self.wrong_letters.add(guessed_letter.lower())
            print(f"Leider nein. Spieler{self.active_player + 1} bekommt {Hangman.WRONG_GUESS_PENALTY} Strafpunkt.")
            print("Ihr habt bereits folgende Buchstaben falsch geraten:", ",".join(sorted(self.wrong_letters)))
            print()

            self.errors[self.active_player] += Hangman.WRONG_GUESS_PENALTY
            self.next_player()

        return State.PLAY_TURN

    def request_solution(self):
        print("Du möchtest lösen! Welches Wort denkst du wird gesucht?")
        return input(">")

    def check_solution(self, solution):
        if solution.lower() == self.word.lower():
            print(f"Das ist das richtige Wort, Gratulation! Spieler{self.active_player + 1} werden {-Hangman.CORRECT_SOLUTION_BONUS} Strafpunkte abgezogen!")
            self.errors[self.active_player] += Hangman.CORRECT_SOLUTION_BONUS
            return State.ANNOUNCE_WINNER
        else:
            clearConsole()
            print(f"{solution} ist leider nicht das gesuchte Wort... Player{self.active_player + 1} bekommt {Hangman.WRONG_SOLUTION_PENALTY} Strafpunkte :(")
            self.errors[self.active_player] += Hangman.WRONG_SOLUTION_PENALTY
            self.next_player()
            return State.PLAY_TURN

    def announce_winners(self):
        winners = self.determine_winners()
        winner_strings = [f'Spieler{i + 1}' for i in winners]
        num_winners = len(winners)

        print("Finaler Punktestand:")
        for player in range(self.num_players):
            print(f"Spieler{player + 1}: ", self.errors[player], " Strafpunkt(e)")

        if num_winners == 1:
            print(f"Gratulation, {winner_strings[0]}, du hast gewonnen!")
        elif 1 < num_winners < self.num_players:
            print(f"Gratulation, {', '.join(winner_strings)}, ihr habt gewonnen!")
        else:
            print("Unentschieden! Ihr seid gleich gut :)")

    def ask_to_play_again(self):
        again = input("Möchtet ihr nochmal spielen? (ja/nein)")
        if again.lower().strip() == "ja":
            return State.START_NEXT_ROUND
        else:
            return State.END

    def determine_winners(self):
        winners = []
        best_score = math.inf
        for i, score in enumerate(self.errors):
            if score == best_score:
                winners.append(i)
            elif score < best_score:
                best_score = score
                winners = [i]
        return winners


def main():
    game = Hangman()
    game.run()


if __name__ == "__main__":
    main()
