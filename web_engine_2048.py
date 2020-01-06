from engine_2048 import *
from grid_2048 import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math
import numpy as np
from Move import EMove


class WebEngine2048:

    def __init__(self):
        """
        Constructor, makes the basic stuff available
        """
        self.browser = webdriver.Safari()
        self.browser.get(url='https://play2048.co/')
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1024, 1024)
        self.htmlElem = self.browser.find_element_by_tag_name('html')
        self.engine2049 = Engine2048()
        self.update()


    def parse_web_content(self):
        """
        Parses the web content to get the cell values.
        """
        # Parse the current score
        try:
            elem = self.browser.find_element_by_class_name('score-container')
            self.engine2049.actualScore = int(elem.text)
            print ('Score: ', elem.text)
        except:
            pass

        G = Grid2048(grid=[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]])

        # Find grid elements:
        for x in range(1,5):
            for y in range(1,5):
                elems = []
                try:
                    elems = self.browser.find_elements_by_class_name('tile-position-'+str(x)+'-'+str(y))
                    max_grid_cell_val = 0

                    if len(elems) > 0:
                        for elem in elems:
                            if (elem != ''):
                                if int(elem.text) > max_grid_cell_val:
                                    max_grid_cell_val = int(elem.text)

                        G.insert(y-1, x-1, max_grid_cell_val)


                except:
                    print('Not found')

        return G


    def move_web_grid(self, move: EMove):
        """
        Sends a command to the browser that moves the grid.
        """
        if move == EMove.LEFT:
            print("Left ----------------------")
            self.htmlElem.send_keys(Keys.LEFT)

        if move == EMove.RIGHT:
            print("Right ----------------------")
            self.htmlElem.send_keys(Keys.RIGHT)

        if move == EMove.UP:
            print("Up ----------------------")
            self.htmlElem.send_keys(Keys.UP)

        if move == EMove.DOWN:
            print("Down ----------------------")
            self.htmlElem.send_keys(Keys.DOWN)


    def update(self):
        """
        Updates the game
        """
        while True:
            G = self.parse_web_content()
            self.engine2049.bestMove = None

            time.sleep(0.1)

            for row in G.grid:
                print(row)
            print("")

            best_score = self.engine2049.alphabeta(G.clone(), 6, -math.inf, math.inf, True)
            best_move = self.engine2049.bestMove
            
            print("Result #######################")
            print(best_score, best_move)

            time_to_sleep = 0.1

            if not G.can_move(best_move):

                if G.can_move(EMove.UP):
                    self.move_web_grid(EMove.UP)
                    time.sleep(time_to_sleep)

                elif G.can_move(EMove.DOWN):
                    self.move_web_grid(EMove.DOWN)
                    time.sleep(time_to_sleep)

                elif G.can_move(EMove.LEFT):
                    self.move_web_grid(EMove.LEFT)
                    time.sleep(time_to_sleep)

                elif G.can_move(EMove.RIGHT):
                    self.move_web_grid(EMove.RIGHT)
                    time.sleep(time_to_sleep)


            else:
                self.move_web_grid(best_move)
                time.sleep(time_to_sleep)



""" MAIN PROGRAM --------------------------------- """

def main():
    webEngine = WebEngine2048()

if __name__ == '__main__':
    main()
