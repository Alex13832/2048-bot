from engine_2048 import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math
from Move import EMove, LinkedMove


class WebEngine2048:

    def __init__(self):
        """
        Constructor, makes the basic stuff available
        """
        self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        self.browser.get(url='https://play2048.co/')
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1024, 1024)
        self.htmlElem = self.browser.find_element_by_tag_name('html')
        self.engine2049 = Engine2048()
        self.has_won_flag = False

        self.update()

    def parse_web_content(self):
        """
        Parses the web content to get the cell values.
        """
        # Parse the current score
        try:
            elem = self.browser.find_element_by_class_name('score-container')
            self.engine2049.actualScore = int(elem.text)
            print('Score: ', elem.text)
        except:
            pass

        G = Grid2048(grid=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

        # Find grid elements:
        for x in range(1, 5):
            for y in range(1, 5):
                elems = []
                try:
                    elems = self.browser.find_elements_by_class_name('tile-position-' + str(x) + '-' + str(y))
                    max_grid_cell_val = 0

                    if len(elems) > 0:
                        for elem in elems:
                            if (elem != ''):
                                if int(elem.text) > max_grid_cell_val:
                                    max_grid_cell_val = int(elem.text)

                        G.insert(y - 1, x - 1, max_grid_cell_val)


                except:
                    print('Not found')

        return G

    def move_web_grid(self, move: EMove):
        """
        Sends a command to the browser that moves the grid.
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
        Updates the game
        """
        while True:
            G = self.parse_web_content()
            self.engine2049.bestMove = None
            self.engine2049.G = G

            if not self.has_won_flag:
                if G.has_won():
                    time.sleep(10)
                    self.browser.find_element_by_css_selector('.keep-playing-button').click()
                    time.sleep(10)
                    self.has_won_flag = True

            time.sleep(0.1)

            print("/////////////////////////////////////")

            lmove = LinkedMove()
            best_score = self.engine2049.alphabeta2(G.clone(), lmove, 3, -math.inf, math.inf, True)
            best_move = self.engine2049.bestMove

            bmove = self.engine2049.linked_move
            m = EMove.CONTINUE

            while bmove.pre_move is not None:
                m = bmove.my_move
                bmove = bmove.pre_move

            print(m, best_move)
            if (m != best_move):
                print("XXXXXXXXXXXXXXXXXXXXXXX")

            time_to_sleep = 0.1

            self.move_web_grid(m)
            # self.move_web_grid(best_move)
            time.sleep(time_to_sleep)


""" MAIN PROGRAM --------------------------------- """


def main():
    webEngine = WebEngine2048()


if __name__ == '__main__':
    main()
