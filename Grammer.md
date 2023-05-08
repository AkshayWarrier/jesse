```java
program        → statement* EOF ;


statement      → exprStmt
               | ifStmt
               | printStmt
               | returnStmt
               | whileStmt
               | block

returnStmt     → "return" expression? ";"

whileStmt      → "the one who knocks" "(" expression ")" statement ";"

ifStmt         → "jesse if" "(" expression ")" statement 
                 ( "else"statement )?

block          → "{" declaration* "}" 

declaration    → funDecl
               | varDecl
               | statement 

funDecl        → "better call " function;
function       → IDENTIFIER "(" parameters? ")" block
parameters     → IDENTIFIER ( "," IDENTIFIER )* ";"

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
unary          → ( "!" | "-" ) unary | call ";"

call           → primary ( "(" arguments? ")" )* ";"
arguments      → expression ( "," expression )* ;

primary        → METH | STRING | "cartel" | "dea" | "i am the danger"
               | "(" expression ")" 
               | IDENTIFIER;
```
