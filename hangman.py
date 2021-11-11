# Simple Hangman Example

import random
import os
import sys

#https://www.delftstack.com/de/howto/python/python-clear-console/
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


class Hangman():

    possible_words = ["Hund", "Waschmaschine", "Quietscheente"]

    def __init__(self):
        self.word = random.choice(Hangman.possible_words).upper()
        self.identified_letters = set([])
        self.wrong_letters = set([])
        self.errors_player1 = 0
        self.errors_player2 = 0
        self.whose_turn = random.choice([1,2])



    def start(self):
        print("Hallo! Willkommen bei Hangman! Möchtest du erst die Regeln erfahren?")
        rules = input(">")
        if rules.lower().strip() == "ja":
            self.explain_rules()
            go = input("Kann es losgehen?")

        clearConsole()
        self.print_current_game_state()
        self.ask_for_letter()


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
        print("Player 1:", self.errors_player1, "Strafpunkt(e)")
        print("Player 2:", self.errors_player2, "Strafpunkt(e)")
        print()



    def ask_for_letter(self):
        print("Player", self.whose_turn, "ist an der Reihe!")
        print("Welchen Buchstaben rätst du?")
        guessed_letter = input(">").upper()


        if len(guessed_letter) != 1:

            if guessed_letter.lower() == "lösen":
                solved = self.solution()
                if solved:
                    self.announce_winner()
                    self.play_again()
                else:
                    self.print_current_game_state()
                    self.ask_for_letter()

            elif guessed_letter.lower() == "regeln":
                self.explain_rules()
                self.print_current_game_state()
                self.ask_for_letter()

            else:
                clearConsole()
                print("Was war das? Wenn du lösen möchtest, schreib bitte 'lösen'! "
                             "Ansonsten verstehe ich nur einzelne Buchstaben :)")
                self.print_current_game_state()
                self.ask_for_letter()


        elif guessed_letter in self.word:
            clearConsole()
            print("Gut geraten!")
            self.identified_letters.add(guessed_letter)

        else:
            self.wrong_letters.add(guessed_letter)
            clearConsole()
            print("Leider nein. Player", self.whose_turn, "bekommt 1 Strafpunkt.")
            print("Ihr habt bereits folgende Buchstaben falsch geraten:", ",".join(sorted(self.wrong_letters)))
            print()

            if self.whose_turn == 1:
                self.errors_player1 += 1
                self.whose_turn = 2
            else:
                self.errors_player2 += 1
                self.whose_turn = 1

        self.print_current_game_state()
        self.ask_for_letter()


    def solution(self):
        print("Du möchtest lösen! Welches Wort denkst du wird gesucht?")
        solution = input(">").upper()
        if solution == self.word:
            print("Das ist das richtige Wort, Gratulation! Player", self.whose_turn, "werden 5 Strafpunkte abgezogen!")
            if self.whose_turn == 1:
                self.errors_player1 -= 5
            else:
                self.errors_player2 -= 5
            return True


        else:
            clearConsole()
            print(solution, "ist leider nicht das gesuchte Wort... Player", self.whose_turn, "bekommt 3 Strafpunkte :(")
            if self.whose_turn == 1:
                self.errors_player1 += 3
                self.whose_turn = 2
            else:
                self.errors_player2 += 3
                self.whose_turn = 1

            return False


    def announce_winner(self):
        winner = None
        if self.errors_player1 < self.errors_player2:
            winner = "Player1"
        elif self.errors_player1 > self.errors_player2:
            winner = "Player2"

        print("Finaler Punktestand:")
        print("Player 1:", self.errors_player1, "Strafpunkt(e)")
        print("Player 2:", self.errors_player2, "Strafpunkt(e)")

        if winner:
            print("Gratulation,", winner, "hat gewonnen!")
        else:
            print("Unentschieden! Ihr seid einfach beide gleich gut :)")

    def play_again(self):
        again = input("Möchtet ihr nochmal spielen?")
        if again.lower().strip() == "ja":
            clearConsole()
            main()
        else:
            print("Okay! Bye-bye!")
            sys.exit()

def main():
    game = Hangman()
    game.start()


if __name__ == "__main__":
    main()
