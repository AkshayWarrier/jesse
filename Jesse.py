from typing import List, Tuple
from Scanner import Scanner
from Parser import Parser
from AstPrinter import AstPrinter
from Interpreter import Interpreter

import sys

class Jesse:
    '''
    Driver class for the Jesse programming language.
    '''
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def run(self, source: str) -> None:
        print("yeah mr white! yeah science!")
        scanner = Scanner(self,source)
        tokens = scanner.scan_tokens()
        parser = Parser(self,source,tokens)
        expr = parser.parse()
        if self.had_error:
            return
        interpreter = Interpreter(self)
        interpreter.interpret(expr)

    def run_file(self, path: str) -> None:
        f = open(path, 'r')
        self.run(f.read())
        f.close()

        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)

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
        self.report_error(code,pos, message)

    def runtime_error(self, error: RuntimeError) -> None:
        print(f'[Runtime Error] {error}')
        self.had_runtime_error = True

    def report_error(self, code:str, pos: Tuple[int,int], message: str) -> None:
        print(code)
        print(" " * pos[1] + '^' + '-'*(len(code) - pos[1] - 1))
        print(f'[Error {pos[0]}] but mr white {message}')
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

    