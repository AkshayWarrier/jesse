# jesse
A programming language for meth heads

## Description
Do you love programming? Are you a Breaking Bad fan? You will love jesse.

jesse is an adaptation of the Lox programming language from the book [Crafting Interpreters](http://www.craftinginterpreters.com/). jesse is almost identical to Lox in structure but makes use of Breaking Bad references as keywords and is implemented in Python.

## Installation
- Clone the repo
```
git clone https://github.com/AkshayWarrier/jesse
cd jesse
```
- Find the `jesse` script in the folder. Create a `.jesse` file and use the script as follows to run your code.
```
python3 jesse Example.jesse
```

## Documentation

### Print Statement
Let's start with printing something on to the screen. To print "heisenberg" on to the screen use
```
say my name "heisenberg";
```
All statements have to end with a `;` otherwise jesse won't be very happy.  A syntax error gets thrown
```
yeah mr white! yeah science!
say my name "heisenberg"
                        ^
[Error 1] mr white where's my semicolon yo?
```

### Variables and Data Types
jesse has a few datatypes one which you have already seen i.e strings. jesse also has another datatype which is uh meth. Meth is always weighed in grams, therefore all meth quantities must be appended with "gm".
Now let's try creating some variables that store meth. To do so use the keyword `cook`
```
cook meth1 = 5gm;
cook meth2 = 10gm;
cook meth3 = 2.5gm;

say my name (meth1*meth2) + meth3;
```
Like you would expect, you can perform all your favourite arthmetic operations on meth.

Null values can be pretty dangerous sometimes therefore they are aptly called `i am the danger`. jesse also supports booleans which are denoted by `cartel` and `dea` for true and false values respectively.

```
// Sets meth to i am the danger
cook meth;

// Prints cartel
say my name dea or cartel;
```

###  Control Flow
jesse supports if else conditions which is almost identical to other languages
```
cook meth = 1000gm;

jesse if (meth >= 1000gm) {
    say my name "We are rich baby!";
} else {
    say my name "We need to cook more meth!";
}
```

On the topic of conditionals, jesse also allows for ternary expressions like some languages
```
cook my_meth = 5gm;

say my name (my_meth > 5gm) ? "More than 5gm of meth" 
                            : "Less than 5gm of meth";
```

jesse supports while loops. To create a while loop use `the one who knocks` keyword. Here's a little program that creates a factorial amount of meth using while loops
```
cook fact_meth = 1gm;
cook n_meth = 5gm;

the one who knocks (n_meth) {
    fact_meth = fact_meth*n_meth;
    n_meth = n_meth - 1gm;
}

say my name fact_meth;
```

I was too lazy to implement for loops

### Functions
To define a function,  use the ``better call`` keyword like so
```
better call saul (){
    say my name "Saul Goodman speedy justice for you!";
}
// Call function
saul();
```

Like in any language, functions may or may not have return values and can take additional parameters as input to the function
```
better call sum(a, b) {
    return (a + b);
}

say my name sum(1gm, 2gm);
```

And what are functions without recursion? Here's a program to produce fibonacci amounts of meth
```
better call fibo(n) {
    jesse if (n == 0gm or n == 1gm) return 1gm;
    return fibo(n - 1gm) + fibo(n - 2gm);
}

say my name fibo(5gm);
```
