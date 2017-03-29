from sudoku import Sudoku
import sys
import getopt


# Process file arguments into sudoku object
def process(arg):
    if type(arg) is not str:
        raise Exception('arguments must be filenames')
    with open(arg, "r") as myfile:
        data = myfile.readlines()
        return Sudoku(data)

# main flow of program
# handles input parsing object and solving
def main():
    # parse sudoku from file
    # parse command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error as msg:
        print(msg)
        print("for help use --help")
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print ('type the path to a file')
            sys.exit(0)
    # solve sudoku
    for arg in args:
        try:
            sudoku = process(arg)
            print("sudoku to solve:".format(sudoku))
            sudoku.solve(False)
            # print(sudoku._smatrix)
        except Exception as error:
            print (error)
    # print sudoku

if __name__ == "__main__":
    main()