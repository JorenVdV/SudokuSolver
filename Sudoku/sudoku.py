from functools import reduce
from math import sqrt, floor
from copy import deepcopy


class Sudoku:
    def __init__(self, stringlist):
        stringlist_cleaned_split = [string.replace("\n","").replace("x", "-1").split(",") for string in stringlist]
        self.__smatrix = [[int(string) for string in string_split]for string_split in stringlist_cleaned_split]
        if sqrt(len(self.__smatrix)) != floor(sqrt(len(self.__smatrix))):
            raise Exception()
        self.__size = len(self.__smatrix)
        self.__blocksize = int(sqrt(self.__size))
        self.__values = list(range(1, self.__size+1))

    def print(self):
        for row in self.__smatrix:
            print(row)

    def solve(self, complex: bool):
        if not complex:
            has_changed = True
            has_options = True
            while not self.__solved() and has_changed:

                has_changed = False

                for row in range(0, self.__size):
                    for column in range(0, self.__size):
                        if self.__smatrix[row][column] == -1:
                            options = self.__solve_element(row, column)

                            if len(options) == 1:
                                self.__smatrix[row][column] = options[0]
                                has_changed = True
                                # print('=========================================UPDATE============================================')
                                # print("({},{}) = {}".format(row, column, options[0]))
                                # self.print()

                            elif len(options) == 0:
                                has_options = False
                                break

                            elif len(options) > 1:
                                has_options = True

                    if not has_options:
                        break

            if not self.__solved() and has_options:
                self.__solve_with_guess()

            elif self.__solved():
                return

            else:
                # self.print()
                raise Exception("Sudoku cannot be solved, without guess")

    def __solve_with_guess(self):
        oldmatrix = deepcopy(self.__smatrix)
        for row in range(0, self.__size):
            for column in range(0, self.__size):
                if self.__smatrix[row][column] == -1:
                    options = self.__solve_element(row, column)
                    for option in options:
                        try:
                            self.__smatrix[row][column] = option
                            self.solve(False) # if this is not the right option it will raise an exception
                            if self.__solved(): # could be left out, I think
                                return
                        except Exception as error:
                            self.__smatrix = oldmatrix

                    if not self.__solved():
                        # self.print()
                        raise Exception("Sudoku cannot be solved")

    def __solve_element(self, row: int, column: int) -> [int]:
        return [x for x in self.__row_options(row)
                if x in self.__column_options(column) and x in self.__block_options(row, column)]

    def __row_options(self, row: int) -> [int]:
        rowvalues = self.__smatrix[row]
        return [x for x in self.__values
                if x not in rowvalues]

    def __column_options(self, column:int) -> [int]:
        columnvalues = [self.__smatrix[row][column] for row in range(0, self.__size)]
        return [x for x in self.__values
                if x not in columnvalues]

    def __block_options(self, row:int, column:int)-> [int]:
        blockvalues = []
        for blockrow in range(row-(row%self.__blocksize), row+(self.__blocksize-row%self.__blocksize)):
            for blockcolumn in range(column-(column%self.__blocksize), column+(self.__blocksize-column%self.__blocksize)):
                blockvalues.append(self.__smatrix[blockrow][blockcolumn])
        return [x for x in self.__values if x not in blockvalues]

    def __solved(self):
        solved_rows = [len(list(filter(lambda smatrix_element: smatrix_element == -1, smatrix_row)))==0 for smatrix_row in
                self.__smatrix]
        return reduce(lambda a, b: a and b, solved_rows, True)
