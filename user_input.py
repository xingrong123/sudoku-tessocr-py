import os
from os.path import isfile, join
from main import readImage

def screenShot():
    mypath = "./images"
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    print("Use snipping tool to take a screenshot of the puzzle and save it in the directory:")
    print("C:\\Users\\teyxi\Documents\\PythonProjects\\SudokuOpenCV\\images")
    onlyfiles2 = []
    while True:
        os.system("SnippingTool")
        onlyfiles2 = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
        
        new_ss_list = []
        for new_ss in onlyfiles2:
            if new_ss not in onlyfiles:
                new_ss_list.append(new_ss)

        if (len(new_ss_list) == 0):
            print("you have not taken a ss. Do you wish to exit? (y/n)")
            i = input()
            if i == "y":
                return
        else:
            break
    
    print(new_ss_list)
    for filename in new_ss_list:
        try:
            puzzle_list = readImage(filename)
            print(puzzle_list)
        except ValueError as err:
            print(err.args)



def main():
    print("Welcome")
    x = ""
    while x != "y" and x != "n":
        print("Do u want to take a ss of a sudoku puzzle? (y/n)")
        x = input().strip()
    if x == "y":
        screenShot()
    
    print("exiting")


if __name__ == "__main__":
    main()

