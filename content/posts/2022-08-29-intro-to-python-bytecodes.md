Title: 銀級贊助商  - Reuven Lerner - An intro to Python bytecodes
Date: 2022-08-29 18:34:00
Category:
Tags: legacy-blogger
Slug: 2022-08-29-intro-to-python-bytecodes
Authors: PyCon Taiwan Blogger contributors

*This was originally posted on blogger [here](https://pycontw.blogspot.com/2022/08/intro-to-python-bytecodes.html)*.
---
One of the most common myths that I encounter in my corporate training is that Python is an interpreted language. It's not really surprising that people believe that -- after all, Python is often referred to as a "scripting" language, and often has the feel of an interpreted language, one that is translated into machine code one line at a time.

But in fact, Python is a byte-compiled language: First, the code that you write is translated into bytecodes -- an interim, portable format that resembles a high-level assembly language. When you run your program, those bytecodes are executed by the Python runtime. This is pretty similar to how things work in a number of other platforms, including .NET and Java -- but the process in Python is so transparent that we often don't think about it.

This is often easiest to see when we define a function. Whenever we use "def", we actually do two things: First, we create a function object. Then we assign that object to a variable.  Both of these seemingly simple steps can be a bit surprising, even to people who have been using Python for many years.

First, the notion that Python has "function objects" seems a bit weird. But really, it's part of Python's overall philosophy that everything is an object. Every string is an instance of class "str", every dictionary is an instance of class "dict", and every function is an instance of class "function". (Note that while both "str" and "dict" are builtin names, "function" is not.) The fact that functions are objects allows us to store them in lists and dicts, and to pass them as arguments to other functions (e.g., the "key" parameter in the builtin "sorted" function). The fact that functions are objects also means that they have attributes, names following dots (.) that act like a private dictionary.

The fact that "def" assigns our newly created function object to a variable is also a bit surprising to many, especially those coming from languages in which functions and data are in separate namespaces. Python has only a single namespace, which means that you cannot have both a variable named "x" and a function named "x" at the same time.

So if I execute the following code in Python:

    def hello(name):

        return f'Hello, {name}!'

I have assigned a new value, a function object, to the variable "hello".  I can even ask Python what type of object the variable refers to, using the "type" builtin:

    >>> type(hello)

    function

It doesn't matter what "hello" might have referred to before; once we have executed "def", the variable "hello" now refers to a function object. We can call our function with parentheses:

    >>> hello('world')

Not surprisingly, we get the following back:

    'Hello, world!'

What happens, though, when we execute our function? In order to understand that, we'll need to have a close look at what is done at compile time (i.e., when we define our function) and at runtime (i.e., when we actually run our function).

I mentioned above that when we define a function, we create a function object, and that the object (like all others in Python) has attributes. The most interesting attribute on a function object is called "\_\_code\_\_" (pronounced "dunder-code" in the Python world, where "dunder" means "double underscore before and after a name"). This is the code object, the core of what is defined when we create a function. The code object itself has a number of attributes, the most interesting of which all start with "co\_".  We can see a full list with the "dir" builtin:

    >>> dir(hello.\_\_code\_\_)

Here's a list of the attributes (a subset of the list that you'll get from running "dir") that start with co\_:

['co\_argcount',

 'co\_cellvars',

 'co\_code',

 'co\_consts',

 'co\_filename',

 'co\_firstlineno',

 'co\_flags',

 'co\_freevars',

 'co\_kwonlyargcount',

 'co\_lines',

 'co\_linetable',

 'co\_lnotab',

 'co\_name',

 'co\_names',

 'co\_nlocals',

 'co\_posonlyargcount',

 'co\_stacksize',

 'co\_varnames']

I wrote above that when we define a function, Python compiles it into bytecodes. Those are stored inside of the co\_code attribute. We can thus see the bytecodes for a function by looking at it:

    >>> print(hello.\_\_code\_\_.co\_code)

The good news is that this works. But the bad news is that it's pretty hard to understand what's going on here:

    b'd\x01|\x00\x9b\x00d\x02\x9d\x03S\x00'

What we see here is a bytestring, a sequence of bytes -- as opposed to a sequence of characters, which is what we would have in a normal Python string. This is the code that Python executes when we run our function.

But wait -- what are these codes? What do they mean, and what do they do? In order to understand, we can use the "dis" function in the "dis" module. That module (and its function) are short for "disassemble," and they allow us to break apart the function and see it:

    >>> import dis

    >>> dis.dis(hello)

      2           0 LOAD\_CONST               1 ('Hello, ')

                  2 LOAD\_FAST                0 (name)

                  4 FORMAT\_VALUE             0

                  6 LOAD\_CONST               2 ('!')

                  8 BUILD\_STRING             3

                 10 RETURN\_VALUE

Things might now start to make more sense, even though we've also opened up a bunch of additional new mysteries.  The (CAPITALIZED) names that we see are the bytecodes, the names of the pseudo-assembly commands that Python recognizes.  The integers to the left of each command indicates the index into co\_code with which each bytecode is associated.

So the byte at index 0 is for LOAD\_CONST. The byte at index 2 is LOAD\_FAST. And the byte at index 4 is FORMAT\_VALUE.

But wait: What do these commands do? And why are we only using the even-numbered bytes?

The LOAD\_CONST instruction tells Python to load a constant value. We're not talking about a constant in the general language, but rather a constant value that was assigned to the function object when it was compiled. At compile time, Python noticed that there was a string, 'Hello, '. It stored that string as a constant on the function object, in a tuple named co\_consts. The function can thus retrieve that constant whenever it needs.  We can, of course, look at the co\_consts tuple ourselves:

    >>> hello.\_\_code\_\_.co\_consts

    (None, 'Hello, ', '!')

As you can see, the element at index 1 in our function's co\_consts is the string 'Hello, '.  So the first bytecode loads that constant, making it available to our Python interpreter.  But wait, where did this constant come from? Look carefully, and you'll see that it's the first part of the f-string that we return in the body of the function. That's right -- while we think of an f-string as a static string with a dynamic component (inside of the {}), Python thinks of it as the combination of static parts (which are stored in co\_consts as strings) and dynamic parts (which are evaluated at runtime).

So our f-string, which looks like this:

    f'Hello, {name}!'

Is turned by the Python compiler into

    'Hello, ' (constant) + name (variable lookup) + '!' (constant)

And indeed, we can see that co\_consts[1] is 'Hello, ', and co\_consts[2] is the single-character string '!'.  In between, we'll need to get the value of the "name" variable.

In order to do this, Python needs to know if "name" is a local variable or a global one. In this case, it's an easy call: Because "name" is a parameter to our function, it is by definition a local variable. Local variable values are retrieved using the LOAD\_FAST bytecode, which we see at byte index 2. But how does it know which local variable to retrieve?

Fortunately, our function object also has an attribute named co\_vars, a tuple of strings with all of the local variable names:

    >>> hello.\_\_code\_\_.co\_varnames

    ('name',)

So the argument 0 which is given to LOAD\_FAST indicates that we want to retrieve the value of local variable 0, aka "name".  In the first two bytecodes, we thus load a constant and a variable name. Then Python uses the special FORMAT\_VALUE bytecode to format our "name" variable:

      2           0 LOAD\_CONST               1 ('Hello, ')

                  2 LOAD\_FAST                0 (name)

                  4 FORMAT\_VALUE             0

Usually, formatting a value means turning it into a string using "str".  But some objects have a special "\_\_format\_\_" method defined, which allows them to have a special output in this context.

We now have two strings on our stack -- and yes, the Python runtime is a stack machine, which you might have learned about if you studied computer science. But we need the exclamation point, so we load that, too:

                6 LOAD\_CONST               2 ('!')

We now have three strings on the stack -- our initial constant, the formatted version of "name", and the constant '!'.  We now create a string, based on these three components, with another bytecode, BUILD\_STRING. We hand BUILD\_STRING an argument of 3, to indicate that it should crate a string from the three topmost items on the stack:

                8 BUILD\_STRING             3

And that's it! We have created the string that we wanted, based on the user's argument. The time has come to return that value, and we do so with the special RETURN\_VALUE bytecode:

               10 RETURN\_VALUE

How often do you really need to read Python bytecodes? Never. But reading the bytecodes does give you a sense of how Python works, what it's doing behind the scenes, how particular functionality (e.g., f-strings) are implemented, and which decisions are made at compile time, rather than runtime.  Understanding Python's division of labor between compile time and runtime can, in my experience, help to make sense of error messages you get, and also to put into context so many other parts of Python that can see mysterious.

I'll be talking about these and other parts of Python bytecodes, especially through the lens of functions, at PyCon APAC 2022, in my talk, "Function dissection lab." I hope to see you there!
