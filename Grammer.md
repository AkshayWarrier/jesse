```python
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
```