from typing import List
import sys

class GenerateAst:
    '''
    Helper function to generate the AST classes

    base_name: The name of the base class
    types: A list of the types of the AST classes that inherit from the base class
    '''
    def define_ast(self, base_name:str, types:List[str], extra_imports:List[str]=[]):
        path = f"{output_dir}/{base_name}.py"
        with open(path, 'w') as f:
            f.write("from typing import List\n")
            f.write("from Token import Token\n\n")
            for import_ in extra_imports:
                f.write(f"from {import_} import {import_}\n")
            f.write("\n")
            f.write(f"class {base_name}:\n")
            f.write("    pass\n")
            for type in types:
                classname = type.split("->")[0].strip()
                fields = type.split("->")[1].strip()
                self.define_type(f, base_name, classname, fields)

    def define_type(self, f:object, base_name:str, classname:str, field_list:str):
        fields = field_list.split(", ")
        f.write(f"\nclass {classname}({base_name}):\n")
        f.write(f"    def __init__(self, {field_list}) -> None:\n")
        for field in fields:
            name,typ = field.split(": ")
            f.write(f"        self.{name} = {name}\n")
        f.write("\n")
        f.write("    def accept(self, visitor):\n")
        f.write(f"        return visitor.visit_{classname.lower()}_{base_name.lower()}(self)\n")




if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1:
        print("Usage: generate_ast <output directory>")
        sys.exit(64)
    output_dir = args[0]
    generator = GenerateAst()
    generator.define_ast("Expr", [
        "Assign   -> name: Token, value: Expr",
        "Ternary  -> condition: Expr, then_branch: Expr, else_branch: Expr",
        "Binary   -> left: Expr, operator: Token, right: Expr",
        "Call     -> callee: Expr, paren: Token, arguments: List[Expr]",
        "Grouping -> expression: Expr",
        "Literal  -> value: object",
        "Logical  -> left: Expr, operator: Token, right: Expr",
        "Unary    -> operator: Token, right: Expr",
        "Variable -> name: Token"
    ])

    generator.define_ast("Stmt", [
        "Block      -> statements: List[Stmt]",
        "Expression -> expression: Expr",
        "BetterCall   -> name: Token, params: List[Token], body: List[Stmt]",
        "JesseIf    -> condition: Expr, then_branch: Stmt, else_branch: Stmt",
        "SayMyName  -> expression: Expr",
        "Return     -> keyword: Token, value: Expr",
        "Cook       -> name: Token, initializer: Expr",
        "TheOneWhoKnocks -> condition: Expr, body: Stmt",
    ], extra_imports=["Expr"])
