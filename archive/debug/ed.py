import os
import sys
import getopt

class LineEditor:
    def __init__(self, filename, verbose):
        self.filename = filename
        self.verbose = verbose
        self.lines = []
        self.load_file()

    def load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.lines = file.readlines()
                return True
        else:
            self.lines = []
            return False

    def save_file(self):
        with open(self.filename, 'w') as file:
            file.writelines(self.lines)

    def view(self):
        for idx, line in enumerate(self.lines, start=1):
            print(f"{idx:03d} |   {line}", end='')

    def edit(self, line_number, new_content):
        if 0 < line_number <= len(self.lines):
            self.lines[line_number - 1] = new_content + '\n'
        else:
            print("Line number out of range.")

    def insert(self, line_number, content):
        if 0 < line_number <= len(self.lines) + 1:
            self.lines.insert(line_number - 1, content + '\n')
        else:
            print("Line number out of range.")

    def delete(self, line_number):
        if 0 < line_number <= len(self.lines):
            self.lines.pop(line_number - 1)
        else:
            print("Line number out of range.")

    def run(self):
        while True:
            command = input("(v)iew, (e)dit, (i)nsert, (d)elete, (l)oad, (s)ave, e(x)it: ").strip().lower()
            if command == "view" or command == "v":
                self.view()
            elif command == "edit" or command == "e":
                line_number = int(input("Enter line number to edit: "))
                new_content = input("Enter new content: ")
                self.edit(line_number, new_content)
            elif command == "insert" or command == "i":
                line_number = int(input("Enter line number to insert at (before): "))
                content = input("Enter content to insert: ")
                self.insert(line_number, content)
            elif command == "delete" or command == "d":
                line_number = int(input("Enter line number to delete: "))
                self.delete(line_number)
            elif command == "load" or command == "l":
                self.filename = input("Enter filename to load file: ")
                f = self.load_file()
                if f:
                    print("File loaded.")
                    self.view()
                else:
                    print("Could not find file.")
            elif command == "save" or command == "s":
                if not self.filename:
                    self.filename = input("Enter filename to save file: ")
                self.save_file()
                print("File saved.")
            elif command == "exit" or command == "x":
                print("Exiting editor.")
                break
            else:
                if self.verbose:
                    print("Help:")
                    print("  view or v for viewing content")
                    print("  edit or e for editing line")
                    print("  insert or i for inserting line")
                    print("  delete or d for deleting line")
                    print("  load or l for loading file")
                    print("  save or s for saving file")
                    print("  exit or x for exiting editor")
                else:
                    print("Unknown command.")

def main(argv):
    inputfile = ''
    verbose = 0

    try:
        opts, args = getopt.getopt(argv,"vhi:",["ifile="])
    except getopt.GetoptError:
        print('ed.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-v':
            verbose = 1
        if opt == '-h':
            print('usage: ed.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
 
    if verbose == 1:
        print("editor ..")
    editor = LineEditor(inputfile, verbose)
    editor.run()
    if verbose == 1:
        print("done.")

if __name__ == "__main__":
   main(sys.argv[1:])