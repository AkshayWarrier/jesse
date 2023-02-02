from typing import List, Tuple
from Scanner import Scanner

import sys

class Jesse:
    '''
    Driver class for the Jesse programming language.
    '''
    def __init__(self):
        self.had_error = False

    def run(self, source: str) -> None:
        print("yeah mr white! yeah science!")
        print()
        scanner = Scanner(self,source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    def run_file(self, path: str) -> None:
        f = open(path, 'r')
        self.run(f.read())
        f.close()

        if self.had_error:
            sys.exit(65)

    def run_prompt(self) -> None:
        while True:
            print('> ', end='')
            try:
                line = input()
            except EOFError:
                break
            self.run(line)
            self.had_error = False

    def error(self, code:str, pos: Tuple[int,int], message: str) -> None:
        self.report(code,pos, '', message)

    def report(self, code:str, pos: Tuple[int,int], where: str, message: str) -> None:
        print(code)
        print(f'mr white theres a problem at line {pos[0]} column {pos[1]}: {message}')
        self.had_error = True


if __name__ == '__main__':
    # Get the command line arguments
    args = sys.argv[1:]
    if len(args) == 0:
        Jesse().run_prompt()
    elif len(args) > 1:
        print('Usage: jesse [script]')
        sys.exit(64)
    elif len(args) == 1:
        Jesse().run_file(args[0])

    