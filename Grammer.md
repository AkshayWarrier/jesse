```python
program        → statement* EOF ;


statement      → exprStmt
               | printStmt
               | block
block          → "{" declaration* "}" 

declaration    → varDecl
               | statement 

varDecl        → "cook" IDENTIFIER ( "=" expression )? ";" 



exprStmt       → expression ";" 
cookStmt       → "cook" expression ";"


expression     → assignment ";"
assignment     → IDENTIFIER "=" assignment";"
               | ternary ";"

ternary        → equality "?" equality ":" equality ";"

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
