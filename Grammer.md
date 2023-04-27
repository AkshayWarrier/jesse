```python
program        → statement* EOF ;


statement      → exprStmt
               | printStmt
               | block;
block          → "{" declaration* "}" ;

declaration    → varDecl
               | statement ;

varDecl        → "cook" IDENTIFIER ( "=" expression )? ";" ;



exprStmt       → expression ";" ;
cookStmt      → "cook" expression ";" ;

expression     → assignment ;
assignment     → IDENTIFIER "=" assignment
               | equality ;

expression     → literal
               | unary
               | binary
               | grouping ;

literal        → METH | STRING | "cartel" | "dea" | "i am the danger" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;

expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → METH | STRING | "cartel" | "dea" | "i am the danger"
               | "(" expression ")" 
               | IDENTIFIER;
```
