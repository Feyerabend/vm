import os
import sys
import getopt
import datetime

class LineEditor:
    def __init__(self, filename, logger, verbose):
        self.filename = filename
        self.logger = logger
        self.lines = []
        self.load_file()

    def load_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.lines = file.readlines()
            self.logger.load(f'NAME = {self.filename}')
            for i, line in enumerate(self.lines):
                self.logger.load(f'{i} = {line}')
            return True
        else:
            self.lines = []
            return False

    def save_file(self):
        with open(self.filename, 'w') as file:
            file.writelines(self.lines)
        self.logger.save(f'NAME = {self.filename}')
        for i, line in enumerate(self.lines):
            self.logger.save(f'{i} = {line}')
        file.close() # ..

    def view(self):
        for idx, line in enumerate(self.lines, start=1):
            print(f"{idx:03d} |   {line}", end='')

    def edit(self, line_number, new_content):
        if 0 < line_number <= len(self.lines):
            self.lines[line_number - 1] = new_content + '\n'
            self.logger.edit(f'{line_number - 1} = {new_content}')
        else:
            print("Line number out of range.")

    def insert(self, line_number, content):
        if 0 < line_number <= len(self.lines) + 1:
            self.lines.insert(line_number - 1, content + '\n')
            self.logger.insert(f'{line_number - 1} = {content}')
        else:
            print("Line number out of range.")

    def delete(self, line_number):
        if 0 < line_number <= len(self.lines):
            self.lines.pop(line_number - 1)
            self.logger.delete(f'{line_number - 1}')
        else:
            print("Line number out of range.")

    def run(self):
        while True:
            command = input("(v)iew, (e)dit, (i)nsert, (d)elete, (l)oad, (s)ave, e(x)it: ").strip().lower()
            if command == "view" or command.startswith("v"):
                self.view()
            elif command == "edit" or command.startswith("e"):
                line_number = int(input("Enter line number to edit: "))
                new_content = input("Enter new content: ")
                self.edit(line_number, new_content)
            elif command == "insert" or command.startswith("i"):
                line_number = int(input("Enter line number to insert at (before): "))
                content = input("Enter content to insert: ")
                self.insert(line_number, content)
            elif command == "delete" or command.startswith("d"):
                line_number = int(input("Enter line number to delete: "))
                self.delete(line_number)
            elif command == "load" or command.startswith("l"):
                self.filename = input("Enter filename to load file: ")
                f = self.load_file()
                if f:
                    print("File loaded.")
                    self.view()
                else:
                    print("Could not find file.")
            elif command == "save" or command.startswith("s"):
                self.save_file()
                print("File saved.")
            elif command == "exit" or command.startswith("x"):
                print("Exiting editor.")
                break
            else:
                print("Unknown command.")
                print("Help:")
                print("  view or v for viewing content")
                print("  edit or e for editing line")
                print("  insert or i for inserting line before")
                print("  delete or d for deleting line")
                print("  load or l for loading file")
                print("  save or s for saving file")
                print("  exit or x for exiting editor")

class Logger:
    def __init__(self, filename, verbose):
        self.filename = filename
        self.verbose = verbose
        self.log_category = {
            'LOAD': 'LOAD',
            'SAVE': 'SAVE',
            'EDIT': 'EDIT',
            'INSERT': 'INSERT',
            'DELETE': 'DELETE'
        }

    def log(self, message, category='LOAD'):
        if category not in self.log_category:
            raise ValueError(f"Invalid log category: {category}")
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} | {category} | {message}"
        if not "\n" in log_message:
            log_message += '\n'
        if os.path.exists(self.filename):
            with open(self.filename, 'a') as file:
                file.write(log_message)
        else:
            print(f"Unable to append to log. Create empty file {self.filename}.")

    def load(self, message):
        self.log(message, category='LOAD')

    def save(self, message):
        self.log(message, category='SAVE')

    def edit(self, message):
        self.log(message, category='EDIT')

    def insert(self, message):
        self.log(message, category='INSERT')

    def delete(self, message):
        self.log(message, category='DELETE')

#
def main(argv):
    inputfile = ''
    logfile = 'log.txt'
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
        print("logger ..")
    logger = Logger(logfile, verbose)
    if verbose == 1:
        print("editor ..")
    editor = LineEditor(inputfile, logger, verbose)
    editor.run()
    if verbose == 1:
        print("done.")

if __name__ == "__main__":
   main(sys.argv[1:])