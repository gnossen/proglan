# Running the Circuit Simulation Test Problem

To run the test problem, use the command

```python bin/proglan examples/wire-test.prog```

All of the possible inputs are present within the file, but commented out.
To run another combination, simply uncomment the desired line. Note that
Python-style line comments are used.

Also note that the import function is used, which inserts the contents of 
```examples/wire.prog``` verbatim into the file. Also, note that ```wire.prog```
imports ```priority-queue.prog```. It's there. I promise.

# Proglan: The Untitled Programming Language

## Everything is an Expression
Proglan follows the philosophy that everything is an expression. Consider the
following code snippet.

```
def f(a) {
    let b = if (a > 0) { 3 } else { 4 }
    b
}

println(f(7))
```

The value of a function is the value of the final expression in the body.

## Function Arguments

The most peculiar feature of Proglan is the particular way in which arguments which
are functions may be passed. While it is possible to pass a closure, you may also use
the following syntax.

```
let sort = def(list)(cmp: a, b) {
    # sort the list with the given comparison
}

sort([5, 23, 345, 2]) { a < b }
sort(["hello", "hola", "aloha", "hi"]) { len(a) < len(b) }
```

In the definition of the sort function, we pass ```list``` as a normal argument. Following
the normal parameter list is a second parenthesized section. This is a final argument which
is defined as having the given named parameters.

When the function ```sort``` is called, a block surrounded by curly braces is appended to the
function call. Within this block, the named parameters ```a``` and ```b``` are inserted into the scope
and the whole block is packaged as a closure and passed as a second argument.

This pattern could conceivably be used in the following fashion.

```
get("/") {
    "{'users': 234, 'status': 'good'}"
}
```

## Objects

Objects are implemented through scopes in Proglan. Consider the following.

```
let Dog = def(name) {
    this.name = name
    this.bark = def() {
        println("Bark!")
    }
    this
}

let dog = Dog("Rover")
dog.bark()
```

The ```this``` keyword refers to the scope of the current function. Elements
in a scope may be accessed using the dot operator. Proglan also supplies the ```new```
keyword, inspired by javascript, which simplifies the above code in the following way.

```
let Dog = def(name) {
    this.name = name
    this.bark = def() {
        println("Bark!")
    }
}

let dog = new Dog("Rover")
dog.bark()
```

Using the ```new``` keyword, the ```Dog``` constructor need not explicity return ```this```.

## No Required Semicolons

Semicolons are not required at the ends of lines. This does mean, however that
newlines occasionally have synactic meaning. For example, the following snippet
is a variable followed by a parenthesized expression.

```
f
(3)
```

While the following snippet is a call to the function ```var_name``` with the
argument ```3```.

```
f(3)
```

If it is desired to put more than one expression on a single line, semicolons
may be used.

```
if (out_of_sync()) { update(); false} else { true }
```

Conversely, if you would like to continue a single expression over multiple lines,
you may use a backslash.

```
def boolean_function() {
    long_function_name() and longer_function_name() and \
        longest_function_name() and longerest_function_name()
}
```

## Import Function

The import function imports a file using a path relative to the file currently being
evaluated, or in the case of the interactive command line, relative to the current
directory. For example, the Dict constructor lives within ```examples/stdlib.prog```

```
import("examples/stdlib.prog")

let dict = new Dict()
dict.add("one", 1)
dict.add("two", 2)
dict.add("three", 3)
println(dict.get("two"))
```

## Drawing Parse Trees

To aid in debugging the parser, there is a utility included in ```bin/parse``` that
will draw the parse tree of an arbitrary Proglan file as a png. Note that this requires
the pydot python package and the graphviz software package.

## Unit Tests

There are a series of unit tests that cover the functionality of the lexer, parser,
and environment. The majority of these tests reference files in the ```examples/```
directory. To run these tests, ensure you have pytest installed, then navigate to the
```proglan/``` subdirectory and run the command ```py.test```. I owe these tests my life.
