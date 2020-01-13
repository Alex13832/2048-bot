import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from engine_2048 import *
from move import *


class WebEngine2048:

    def __init__(self):
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        self.browser.get(url='https://play2048.co/')
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1024, 1024)
        self.htmlElem = self.browser.find_element_by_tag_name('html')
        self.engine2048 = Engine2048()
        self.actual_score = 0
        self.has_won_flag = False

        self.update()

    def parse_web_content(self):
        """
        Parses the 2048 game in the Web-browser.
        :return: parsed game.
        """
        # Parse the current score
        try:
            elem = self.browser.find_element_by_class_name('score-container')
            self.actual_score = int(elem.text)
            print('Score: ', elem.text)
        except:
            pass

        game = Grid2048()

        range_str = ["1", "2", "3", "4"]

        # Parse the grid
        for x in range_str:
            for y in range_str:
                try:
                    elements = self.browser.find_elements_by_class_name('tile-position-' + x + '-' + y)
                    max_grid_cell_val = 0

                    if len(elements) > 0:
                        for elem in elements:
                            if elem != '':
                                if int(elem.text) > max_grid_cell_val:
                                    max_grid_cell_val = int(elem.text)

                        game.insert(int(y) - 1, int(x) - 1, max_grid_cell_val)

                except:
                    print('Not found')

        return game

    def move_web_grid(self, move: EMove):
        """
        Moves the game in the web browser.
        :param move: Left, Right, Up or Down.
        :return:
        """
        if move == EMove.LEFT:
            self.htmlElem.send_keys(Keys.LEFT)

        if move == EMove.RIGHT:
            self.htmlElem.send_keys(Keys.RIGHT)

        if move == EMove.UP:
            self.htmlElem.send_keys(Keys.UP)

        if move == EMove.DOWN:
            self.htmlElem.send_keys(Keys.DOWN)

    def update(self):
        """
        Gets the parsed game and then runs the AI to get best move that will be used to move the
        game in the next direction.
        :return:
        """
        nbr_runs = 1
        wins, scores = [], []

        for i in range(nbr_runs):

            while True:
                G = self.parse_web_content()
                self.engine2048.bestMove = None

                if not self.has_won_flag:
                    if G.has_won():
                        time.sleep(5)
                        self.browser.find_element_by_css_selector('.keep-playing-button').click()
                        time.sleep(5)
                        self.has_won_flag = True
                        wins.append(1)

                time.sleep(0.1)

                print("///////////////////////////////////// Iteration", i, " Score", self.actual_score)

                # best_move = self.engine2048.best_move_alpha_beta(G, 5)
                best_move = self.engine2048.best_move_expectimax(G, 4)

                self.move_web_grid(best_move)
                time.sleep(0.2)

                if best_move is None:
                    break

            # ////////////////////////// STATS /////////////////////////////////
            scores.append(self.actual_score)
            self.actual_score = 0

            # ////////////////////////// NEW GAME //////////////////////////////
            if i < nbr_runs:
                time.sleep(2)
                self.browser.find_element_by_css_selector('.restart-button').click()
                self.has_won_flag = False
                time.sleep(2)

        print("///////////////// STATS ////////////////////////")
        print("Number of wins ", sum(wins))
        print("Win probability ", sum(wins) / nbr_runs)
        print("smallest score", min(scores))
        print("Highest score ", max(scores))
        print("Average score ", sum(scores) / nbr_runs)
        print("Scores", scores)
        print("Wins", wins)


""" MAIN PROGRAM --------------------------------- """


def main():
    WebEngine2048()


if __name__ == '__main__':
    main()
