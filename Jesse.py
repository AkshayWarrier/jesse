from typing import Tuple
from Scanner import Scanner
from Parser import Parser
from Interpreter import Interpreter
from Resolver import Resolver

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
        if self.had_error:
            return

        parser = Parser(self,source,tokens)
        statements = parser.parse()
        if self.had_error:
            return
        interpreter = Interpreter(self,source)
        resolver = Resolver(self,source,interpreter)
        resolver.resolve(statements)
        if self.had_error:
            return
        interpreter.interpret(statements)

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
        self.report_error(code,pos,message)

    def runtime_error(self, code:str, pos: Tuple[int,int], error: RuntimeError) -> None:
        print(code)
        print(" " * pos[1] + '^' + '-'*(len(code) - pos[1] - 1))
        print(f'[Runtime Error {pos[0]}] mr white {error}')
        self.had_runtime_error = True

    def report_error(self, code:str, pos: Tuple[int,int], message: str) -> None:
        print(code)
        print(" " * pos[1] + '^' + '-'*(len(code) - pos[1] - 1))
        print(f'[Error {pos[0]}] mr white {message}')
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

    