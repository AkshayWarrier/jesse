```python
program        → statement* EOF ;


statement      → exprStmt
               | ifStmt
               | printStmt
               | block

ifStmt         → "cook" "(" expression ")" statement ( "else" statement )?

block          → "{" declaration* "}" 

declaration    → varDecl
               | statement 

varDecl        → "cook" IDENTIFIER ( "=" expression )? ";" 



exprStmt       → expression ";" 
cookStmt       → "cook" expression ";"


expression     → assignment ";"
assignment     → IDENTIFIER "=" assignment";"
               | logic_or ";"

logic_or       → logic_and ( "or" logic_and )* ;
logic_and      → ternary ( "and" ternary )* ;

ternary        → equality
               | equality "?" equality ":" equality ";"

equality       → comparison ( ( "!=" | "==" ) comparison )* ";"
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ";"
term           → factor ( ( "-" | "+" ) factor )* ";"
factor         → unary ( ( "/" | "*" ) unary )* ";"
unary          → ( "!" | "-" ) unary";"
               | primary ";"
primary        → METH | STRING | "cartel" | "dea" | "i am the danger"
               | "(" expression ")" 
               | IDENTIFIER;
```
