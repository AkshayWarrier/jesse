from typing import List
import sys

class GenerateAst:
    '''
    Helper function to generate the AST classes

    base_name: The name of the base class
    types: A list of the types of the AST classes that inherit from the base class
    '''
    def define_ast(self, base_name:str, types:List[str]):
        path = f"{output_dir}/{base_name}.py"
        with open(path, 'w') as f:
            f.write("from typing import List\n")
            f.write("from Token import Token\n\n")
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
        "Binary   -> left: Expr, operator: Token, right: Expr",
        "Grouping -> expression: Expr",
        "Literal  -> value: object",
        "Unary    -> operator: Token, right: Expr",
    ])

    generator.define_ast("Stmt", [
        "Expression -> expression: Expr",
        "Print      -> expression: Expr",
    ])
