from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Grid2048:

    def __init__(self):
        """
        Constructor, sets all element to 0
        """
        self.grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]] # Rows


    def is_power2(self, num):
    	'states if a number is a power of two'
    	return num != 0 and ((num & (num - 1)) == 0)


    def update_grid(self, x, y, newVal):
        """
        Sets position x, y to newVal
        """
        self.grid[x-1][y-1] = newVal


    def move(self, row):
        score = 0

        row1 = list(filter(lambda a: a != 0, row))
        row1.append(1)
        row2 = []

        while len(row1) > 1:
            a = row1.pop(0)
            if row1[0] == a:
                row2.append(2*a)
                row1.pop(0)
            else:
                row2.append(a)

        for i in range(4-len(row2)):
            row2.append(0)


    def move_rev(self, row):
        row2 = move(row[::-1])
        return row2[::-1]


    def move_left(self):
        for row in self.grid:
            row = self.move(row)


    def move_right(self):
        for row in self.grid:
            row = self.move_rev(row)


    def move_up(self):
        """
        Calculates max score if board is move vertically.
        """
        max_points = 0

        col0 = [item[0] for item in self.grid]
        col1 = [item[1] for item in self.grid]
        col2 = [item[2] for item in self.grid]
        col3 = [item[3] for item in self.grid]


    def print_grid(self):
        """
        Prints all elements in the grid.
        """
        for row in self.grid:
            for val in row:
                print(str(val) + " ", end="")

            print("")



# Creates a Firefox webbrowser
browser = webdriver.Safari()
# Open 2048 html page
browser.get(url='https://play2048.co/')
# browser.get(url='https://gabrielecirulli.github.io/2048/')
htmlElem = browser.find_element_by_tag_name('html')
# Game board
grid = Grid2048()

move = ''

while (True):
    grid = Grid2048()

    # Find grid elements:
    for x in range(1,5):
        for y in range(1,5):
            elems = []
            try:
                elems = browser.find_elements_by_class_name('tile-position-'+str(x)+'-'+str(y))
                max_grid_cell_val = 0

                if len(elems) > 0:
                    for elem in elems:
                        if (elem != ''):
                            if int(elem.text) > max_grid_cell_val:
                                max_grid_cell_val = int(elem.text)

                    grid.update_grid(y, x, max_grid_cell_val)


            except:
                print('Not found')

    # Get scores
#    score_h = grid.get_max_score_horizontally()
#    score_v = grid.get_max_score_vertically()
    score_h = 0
    score_v = 0

    if score_h == 0 and score_v == 0:
        htmlElem.send_keys(Keys.UP)
        time.sleep(0.2)
        htmlElem.send_keys(Keys.DOWN)

    elif score_h >= score_v:
        htmlElem.send_keys(Keys.LEFT)

    elif score_v > score_h:
        htmlElem.send_keys(Keys.DOWN)


    time.sleep(0.2)



browser.quit()
