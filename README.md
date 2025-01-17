# `pdb` and Debugging Lab

This lab has two functions:
1. To teach you the basics of `pdb`, the **P**ython **D**e**B**ugger for
[Python2](https://docs.python.org/2/library/pdb.html) and
[Python3](https://docs.python.org/3/library/pdb.html), including some helpful
tricks to make your debugging sessions a lot less stressful.
2. To practice a couple of ways to use the `unittest` library to build,
well, unit tests for the debugged code!

Part 1 is adopted from user spside's
[Debugging Lab](https://github.com/spiside/pdb-tutorial). Part 2 is authored
by Prof. Xanda for CS 123 at HMC.

# Part 1: PDB Tutorial
*Written by spside, some edits by Prof. Xanda*

## What is the purpose of a debugger?

Why use a debugger? With a debugger, you can:
* Explore the state of a running program
* Follow the program's execution logic
* (in interpreted languages) Test implementation code before applying it

Why not just use `print()`? Print statements require you to decide
every condition you want to check before the program starts running. For small
and fast programs, that may be realistic and efficient - but for a program 
that takes twenty minutes to get to the point where it breaks, or one where
there are lots of functions and variables in play, it might not be realistic
to print out all possible relevant variables all the time!

In contrast, when you use a debugger, you can set a
[breakpoint](https://en.wikipedia.org/wiki/Breakpoint) at any point of your
program to stop it and apply the three points above. Debuggers are very powerful
tools, especially in interpreted languages, because they allow you not just to
go through the code slowly and inspect whatever you want as you find your bug ,
but to decide in real time what information you need and what code snippet might
fix a problem *as the program is running*!

In this tutorial, we're going to look at a little messy program, one you could
probably debug with just print statements -- but we're going to use that as
a low-stress place to get a little more comfortable using a debugger. Hopefully
this will allow you to use in your own Python code!

## Playing the Game

Your boss has given you the following project to fix for a client. It's supposed
to be a simple dice game, where the object of the game is to correctly add up
the values of the dice for 6 consecutive turns.

The issue is that a former programmer worked on it who didn't know how to debug
effectively. It's now up to you to clean up this code and add tests.

To get started, clone this repo if you haven't already done so following the lab
instructions.

```shell
cd /path/to/debugging-testing-lab
```

To begin, let's try playing the game to see what's wrong. To run the program,
type the following in your terminal:

```shell
python main.py
``` 

You should see something like this:

```
Add the values of the dice
It's really that easy
What are you doing with your life.
Round 1

---------
|*      |
|       |
|      *|
---------
---------
|*      |
|       |
|      *|
---------
---------
|*     *|
|       |
|*     *|
---------
---------
|*     *|
|       |
|*     *|
---------
---------
|*     *|
|   *   |
|*     *|
---------
Sigh. What is your guess?: 
```

Seems like the previous programmer had a sense of...humor? Nonetheless, let's
enter 17 (since that is the total value of the dice).

```
Sigh. What is your guess?: 17
Sorry that's wrong
The answer is: 5
Like seriously, how could you mess that up
Wins: 0 Loses 1
Would you like to play again?[Y/n]: 
```

Weird. It said the answer is 5 but that's clearly wrong. Let's play the game
again to figure it out. Looks like the prompt to play again is `'Y'` so let's
enter that now.

```
Would you like to play again?[Y/n]: Y
Traceback (most recent call last):
  File "main.py", line 12, in <module>
    main()
  File "main.py", line 8, in main
    GameRunner.run()
  File "/Users/Development/pdb-tutorial/dicegame/runner.py", line 62, in run
    i_just_throw_an_exception()
  File "/Users/Development/pdb-tutorial/dicegame/utils.py", line 13, in i_just_throw_an_exception
    raise UnnecessaryError("You actually called this function...")
dicegame.utils.UnnecessaryError: You actually called this function...
```

Weird. The code threw a hard-to-read exception even though we used what was
supposed to be a valid input. So we have at least two bugs to fix: making the
dice addition correct, and making sure the play-again prompt is responsive.

I think it's safe to say that the program is broken. Let's start the debugging
process! 


## PDB 101: Intro to `pdb`

It's time to work with python's very own debugger `pdb`. The debugger is
included in python's standard library, and we use it the same way we would with
any python library. First, we have to import the `pdb` module; then, we call one
of its methods to add a debugging breakpoint in the program.

Historically, the conventional way to do this is to add the import **and** call
the method at the same line you would like to stop at. (While you don't usually
do this for permanent code, this helps to make sure that you don't leave the
import to pdb in once you're done debugging.) This is the full statement you
would want to include:

```python
import pdb; pdb.set_trace()
```

(Note: Starting from Python 3.7, the built-in function `breakpoint()` can be
used instead of using `import pdb; pdb.set_trace()`!)

The methods
[`set_trace()`](https://docs.python.org/3/library/pdb.html#pdb.set_trace) and
[`breakpoint()`](https://docs.python.org/3/library/functions.html#breakpoint)
hard code a breakpoint where the method was called. Let's use the `set_trace()`
method for this tutorial since it is supported in all python versions. Let's try
it now by opening up the `main.py` file and adding a breakpoint on line 8:

`file: main.py` 
```python
from dicegame.runner import GameRunner


def main():
    print("Add the values of the dice")
    print("It's really that easy")
    print("What are you doing with your life.")
    import pdb; pdb.set_trace() # add pdb here
    GameRunner.run()


if __name__ == "__main__":
    main()
```

Cool, now let's try to run `main.py` again and see what happens.

```shell
python main.py
```
```
Add the values of the dice
It's really that easy
What are you doing with your life.
> /Users/Development/pdb-tutorial/main.py(9)main()
-> GameRunner.run()
(Pdb) 
```

There we go! We have started our own little read-eval-print-ing interpreter
right after line 8 ran, so we can start poking around. It seems like the first
issue we should solve is the proper summation of the dice values.

If you are familiar using IPython (interactive Python), a lot of that knowledge
can be transferred to the `pdb` debugger. However, there will be a couple
gotchas that we will get to in the advanced section. Regardless, let's learn a
couple commands that will help us solve the addition issue.


## The 5 `pdb` commands that will leave you "speechless"

Taken directly from the `pdb` documentation, these are the five commands that,
once you learn them, you won't know how you lived without them.

1. `l(ist)` - Displays 11 lines around the current line or continue the previous listing.
2. `s(tep)` - Execute the current line, stop at the first possible occasion.
3. `n(ext)` - Continue execution until the next line in the current function is reached or it returns.
4. `b(reak)` - Set a breakpoint (depending on the argument provided).
5. `r(eturn)` - Continue execution until the current function returns.

Notice that there are brackets around the last part of every keyword. The
brackets indicate that the rest of the word is _optional_ when using the command
prompt for `pdb`. This saves typing, but a major gotcha is if you have a
variable name such as `l` or `n`, then the `pdb` command takes precedence. That
is, say you have a variable named `c` in your program and you want to know the
value of `c`. Well, if you type `c` in `pdb`, you will actually be issuing the
`c(ontinue)` keyword which executes the program and only stops if it encounters
a break point! (The best way to avoid this is just to use more expressive
variable names, which you really should do anyways!)

**NB**: Another helpful tool is the following:
`h(elp) - Without argument, print the list of available commands. With a command as an argument, print help about that command.`

For the rest of the tutorial, I will be using the shortened version of the
commands and if I use a command that I have not introduced here, I will explain
what it does. So, let's begin with the first one.

### 1. l(ist) a.k.a. I'm too lazy to open the file containing the source code

```
(Pdb) help l
l(ist) [first [,last]]
    List source code for the current file. Without arguments, list 11 lines around the current line
    or continue the previous listing. With one argument, list 11 lines starting at that line.
    With two arguments, list the given range; if the second argument is less than the first, it is a count.
```

Using `list`, we can examine the source code of the current file we are in. The
arguments for `list` lets you specify a given range of lines you wish to see
which can be helpful if you are in some weird 3rd party package and you are
trying to figure out why they can't get string encoding working _true story_.

**NB**: In Python 3.2 and above, you can type `ll` (long list) which shows you
source code for the current function or frame. I use this all the time instead
of `l` since it's much better knowing which function you are in than an
arbitrary 11 lines around your current position.

Let's try using `l` now. In your already open `pdb` prompt, type in `l` and look
at the output:

```
(Pdb) l
  4     def main():
  5         print("Add the values of the dice")
  6         print("It's really that easy")
  7         print("What are you doing with your life.")
  8         import pdb; pdb.set_trace()
  9  ->     GameRunner.run()
 10     
 11     
 12     if __name__ == "__main__":
 13         main()
[EOF]
``` 

If we want to see the whole file, we can call the list function with the range 1
to 13 like so:

```
(Pdb) l 1, 13
  1     from dicegame.runner import GameRunner
  2     
  3     
  4     def main():
  5         print("Add the values of the dice")
  6         print("It's really that easy")
  7         print("What are you doing with your life.")
  8         import pdb; pdb.set_trace()
  9  ->     GameRunner.run()
 10     
 11     
 12     if __name__ == "__main__":
 13         main()
```

Unfortunately, we don't get that much information from this file alone but we do
see that it is calling the `run()` method of the `GameRunner` class. At this
point, you might be thinking, "Awesome, I'll just set a `pdb` in the run method
in the `dicegame/runner.py` file !" That will work, but there's an even easier
way using the `step` command we will discuss next.

### 2. `s(tep)` a.k.a let's see what this method does...

```
s(tep)
    Execute the current line, stop at the first possible occasion
    (either in a function that is called or in the current
    function).
```

Your current line of execution should still be on `:9` and you can tell the
current line by looking at the `->` outputted by the `list` command. Let's call
the `step` command and see what happens.

```
(Pdb) s
--Call--
> /Users/Development/pdb-tutorial/dicegame/runner.py(21)run()
-> @classmethod
```

Nice! We're currently in the `runner.py` file on line 21, which we can tell from
this line: `> /Users/Development/pdb-tutorial/dicegame/runner.py(21)run()`. The
problem is, we haven't seen that code yet. Run the `list` command to see the
method.

```
(Pdb) l
 16             total = 0
 17             for die in self.dice:
 18                 total += 1
 19             return total
 20     
 21  ->     @classmethod
 22         def run(cls):
 23             # Probably counts wins or something.
 24             # Great variable name, 10/10.
 25             c = 0
 26             while True:
```

Awesome! Now we have some more context on the `run()` method, but we are
currently on line `:21`. Let's `step` in one more time so that we enter the
method itself and then run the list command to see our current position.

```
(Pdb) s
> /Users/Development/pdb-tutorial/dicegame/runner.py(25)run()
-> c = 0
(Pdb) l
 20     
 21         @classmethod
 22         def run(cls):
 23             # Probably counts wins or something.
 24             # Great variable name, 10/10.
 25  ->         c = 0
 26             while True:
 27                 runner = cls()
 28     
 29                 print("Round {}\n".format(runner.round))
 30  
```

As we can see, we are on a terribly named `c` variable that will cause us a
major issue if we try to call it. We are just before the `while` loop so let's
enter the loop and see what else we can uncover.

### 3. `n(ext)` a.k.a I hope this current line doesn't throw an exception

```
n(ext)
    Continue execution until the next line in the current function
    is reached or it returns.
```

From the current line, type the `n(ext)` command followed by `list` (notice a
pattern) and let's observe what happens.

**NB**: `n(ext)` allows you to skip over function calls while `s(tep)` allows
you to step into a function call and pause at the first line of the called
function.

```
(Pdb) n
> /Users/Development/pdb-tutorial/dicegame/runner.py(27)run()
-> while True:
(Pdb) l
 21         @classmethod
 22         def run(cls):
 23             # Probably counts wins or something.
 24             # Great variable name, 10/10.
 25             c = 0
 26  ->         while True:
 27                 runner = cls()
 28     
 29                 print("Round {}\n".format(runner.round))
 30     
 31                 for die in runner.dice:
```

Now our current line on the `while True` statement! We can keep calling `next`
indefinitely until the program throws an exception or terminates. Call `next` 3
more times to get to the `for` loop and then follow up `next` with `list`.

```
(Pdb) n
> /Users/Development/pdb-tutorial/dicegame/runner.py(27)run()
-> runner = cls()
(Pdb) n
> /Users/Development/pdb-tutorial/dicegame/runner.py(29)run()
-> print("Round {}\n".format(runner.round))
(Pdb) n
Round 1

> /Users/Development/pdb-tutorial/dicegame/runner.py(31)run()
-> for die in runner.dice:
(Pdb) l
 26             while True:
 27                 runner = cls()
 28     
 29                 print("Round {}\n".format(runner.round))
 30     
 31  ->             for die in runner.dice:
 32                     print(die.show())
 33     
 34                 guess = input("Sigh. What is your guess?: ")
 35                 guess = int(guess)
```

At this current point, if you continue to type the `next` command you will then
iterate through the `for` loop for the length of the `runner.dice` attribute. We
can take a look at the length of the `runner.dice` by calling the `len()`
function around it in the `pdb` REPL which should return 5.

```
(Pdb) len(runner.dice)
5
```

Since the length is _only_ 5 items, we could iterate through the loop by calling
`next` 5 times, but let's say there were 50 items to iterate over, or even
10,000! A better option would be to set a break point and then `continue` to
that break point instead.


### 4. `b(reak)` a.k.a I don't want to type `n` anymore

```
b(reak) [ ([filename:]lineno | function) [, condition] ]
    Without argument, list all breaks.

    With a line number argument, set a break at this line in the
    current file.  With a function name, set a break at the first
    executable line of that function.  If a second argument is
    present, it is a string specifying an expression which must
    evaluate to true before the breakpoint is honored.

    The line number may be prefixed with a filename and a colon,
    to specify a breakpoint in another file (probably one that
    hasn't been loaded yet).  The file is searched for on
    sys.path; the .py suffix may be omitted.
```

We're only going to pay attention to the first two paragraphs of `b(reak)`'s
description in this tutorial. Like I mentioned in the previous section, we want
to set a break point past the `for` loop so we can continue to navigate through
the `run()` method. Let's stop on `:34` since this has the input function which
will break and wait for a user input anyways. To do this, we can type `b 34` and
then `continue` to the break point.

```
(Pdb) b 34
Breakpoint 1 at /Users/Development/pdb-tutorial/dicegame/runner.py(34)run()
(Pdb) c

[...] # prints some dice

> /Users/Development/pdb-tutorial/dicegame/runner.py(34)run()
-> guess = input("Sigh. What is your guess?: ")
```

We can also take a look at the break points that we have set by calling `break`
without any arguments.

```
(Pdb) b
Num Type         Disp Enb   Where
1   breakpoint   keep yes   at /Users/Development/pdb-tutorial/dicegame/runner.py:34
    breakpoint already hit 1 time
```

To clear your break points, you can use the `cl(ear)` command followed by the
breakpoint number which is found in the leftmost column of the above output.
Let's clear the breakpoint now by calling the `clear` command followed by 1.

**NB**: You can also clear all the breakpoints if you don't provide any
arguments to the `clear` command.

```
(Pdb) cl 1
Deleted breakpoint 1 at /Users/Development/pdb-tutorial/dicegame/runner.py:34
```

From here we can call `next` and execute the `input()` function. Let's just type
10 for our guess and once we are back in the `pdb` REPL, call `list` so we can
see the next few lines.

```
(Pdb) n
Sigh. What is your guess?: 10
> /Users/Development/pdb-tutorial/dicegame/runner.py(35)run()
-> guess = int(guess)
(Pdb) l
 30     
 31                 for die in runner.dice:
 32                     print(die.show())
 33     
 34                 guess = input("Sigh. What is your guess?: ")
 35  ->             guess = int(guess)
 36     
 37                 if guess == runner.answer():
 38                     print("Congrats, you can add like a 5 year old...")
 39                     runner.wins += 1
 40                     c += 1


``` 

Remember that we are trying to find out why our guess wasn't correct on our
first playthrough. It seemed like there was an error with the `guess ==
runner.answer` equality condition. We should check to see what the
`runner.answer()` method is doing in case there might be an error there. Call
`next` and then let's call `step` to _step_ into the `runner.answer()` method.

```
(Pdb) s
--Call--
> /Users/spiro/Development/mobify/engineering-meeting/pdb-tutorial/dicegame/runner.py(15)answer()
-> def answer(self):
(Pdb) l
 10         def reset(self):
 11             self.round = 1
 12             self.wins = 0
 13             self.loses = 0
 14     
 15  ->     def answer(self):
 16             total = 0
 17             for die in self.dice:
 18                 total += 1
 19             return total
 20  
```

I think I found the issue! On line 18, it doesn't look like the `total` variable
is adding up the values of the dice like we want it to. Let's see if we can fix
that by checking whether a `die` has an attribute which would contain its value.
To get to line 18, you can either set a break point or just call `next` until
you hit the first iteration. Once you're on `:18`, let's call the `dir()`
function on the `die` instance and check what methods and attributes it has.

```
-> total += 1
(Pdb) dir(die)
['__class__', '__delattr__', [...], 'create_dice', 'roll', 'show', 'value']
``` 

There is a `value` attribute after all! Let's call that and see what returns
(remember, this value will probably be different than mine). And just for fun,
let's make sure it is equal to the value that the die is showing by calling the
`show()` method as well.

```
(Pdb) die.value
2
(Pdb) die.show()
'---------\n|*      |\n|       |\n|      *|\n---------'
```

**NB**: If you want the newline character `\n` to print as a newline, call
`print(die.show())`.

It looks like it works as expected and we're ready to fix the answer method.
However, some of us may want to continue with the debugging process and catch
all the errors in one go. Unfortunately, we are once again stuck in this for
loop. You might think to set a break point at `:19` and then call `continue` but
there is actually a better way in this case.

### 5. `r(eturn)` a.k.a. I want to get out of this function

```
r(eturn)
    Continue execution until the current function returns.
```

The `return` lets you skip ahead to examine the final outcome of a function.
While you could set a breakpoint at the return call, the `return` pdb command
will help if there are multiple return statements in a single function since it
only follows the path of execution for where it returns on that call. Let's call
the `return` command and get to the end of the function.

```
(Pdb) r
--Return--
> /Users/Development/pdb-tutorial/dicegame/runner.py(19)answer()->5
-> return total
(Pdb) l
 14     
 15         def answer(self):
 16             total = 0
 17             for die in self.dice:
 18                 total += 1
 19  ->         return total
 20     
 21         @classmethod
 22         def run(cls):
 23             # Probably counts wins or something.
 24             # Great variable name, 10/10.
(Pdb) 
```

To check the value of the returned `total` variable, you can call `total` here
or look at the final value in line below the `--Return--` output. Now, to return
back to the `run()` method, call the `next` command and you'll be back in your
happy place.

At this point, you can exit the `pdb` debugger by calling `exit()` **OR**
`CTRL+D` (same as the Python REPL). With these five commands, you should be able
to figure out a couple other bugs and then follow along with a bit more advanced
`pdb` examples. **Put each issue you fix in your list of issues in Que
instructions.txt. P

[Prof. X]: That concludes part one - thanks again to user spside for making a
[fun and tidy example repo](https://github.com/spiside/pdb-tutorial) for pdb! If
you're interested in more detail, you can check out the original tutorial for
notes about the `!` (bang) command, the `commands` command, and the `postmortem`
command. If you want a fancier option than pdb, you can also explore the
installable [ipdb](https://pypi.org/project/ipdb/) library for Python -- it has
a few neat features, including `launch_ipdb_on_exception():` context manager for
when you're having trouble tracking a bug!

# Part II. Testing Tutorial

*This part is unique to CS 123 and authored by Prof. Xanda.*

Now that you've debugged, it'd be nice to add some tests. Choose at least three
behaviors to test, including:
* at least one test that tests that a bug you fixed remains fixed,
* at least one test that verifies that the runner works correctly end-to-end.
Put the list of bugs you fix in instructions.txt under the second question.

## Testing with unittest

There are a number of different Python resources that exist to help automate
tests. One module built in to Python is called `unittest`, which has classes
containing methods that support standard functionality you'd want to write
tests, including nice assert statements to compare values, built-in
functionality to `setUp` and `tearDown` objects and data for complex tests, and
support to `mock` out fake objects, functions, etc. when you want to mimic parts
of your codebase instead of calling into complex/slow/resource
intensive/unpredictable code.

Right now, there's one test, which you can see in `tests/test_die.py`. It exists
inside the `TestDie` class following a standard pattern for creating tests in
`unittest`. You can follow this template to make a test file for `runner.py` as
well - that is, you can make a new Python file `test_runner`, make a class
`TestRunner` inheriting from `unittest.TestCase`, and write test case functions
whose names start with `test_` inside that class. You should be able to import
code from the local `dicegame` package, which is the package name for your
codebase.

If you want to run all the tests, you can navigate to the top-level directory of
the repository and run ```python3 -m unittest``` to run all of the tests that
can be discovered in the directory. It'll automatically discover all of the
tests in the folder. If you want to run subparts, you can add information about
where a specific file, class, or test is, e.g. ```python -m unittest
tests.test_die.TestDie.test_valid ```

(Note: the reason `unittest` works with no arguments has to do with telling
Python that the `tests` folder is a module. We do this by putting in a file
called `__init__.py` in the folder - in this case, a totally empty file.
We're not going into why this matters, but if you have trouble getting
`unittest` to work in another project, `__init__.py` may have something to
do with it.)

You should add tests to `test_die.py` and/or `test_runner.py` based on which
components you are testing.
Here are some good starting points to see examples of tests, with some more
advice from me below:
* [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
* [DataQuest tutorial for unit tests](https://www.dataquest.io/blog/unit-tests-python/)
* [Introduction to mocking in Python](https://www.toptal.com/python/an-introduction-to-mocking-in-python)
* (Advanced) [Python examples of mock](https://docs.python.org/3/library/unittest.mock-examples.html)

## Managing complex code

Right now, we have a lot of factors that are hard for us to test our runner
easily for a couple of reasons: one, that our game includes randomness, and two,
that it requires user input. Both of these problems can be addressed in unit
tests!

### Limiting randomness
To help with random dice rolls, we may want to ensure our random number
generator always performs the same way. We can do this by calling the
`random.seed(s)` function with some defined constant integer `s` that's part of
our test case.

```
def test_thing(self):
    random.seed(0)
    # code that does something with dice
```

This is useful because the `random` module isn't really random - it's
pseudorandom, and that randomness depends on a seed number. When we reset that
seed to the same number every time, like 0, we expect the same sequence of
random numbers each time. Thus, this test will always produce the same dice. (In
this case, it's important to seed the randomness in the test, otherwise it might
depend on the sequence that tests are run!)

In practice, this will make the test predictable for now...but if we did
something that added a new random number generation step in between generating
dice, it's possible that would change our list of dice. Suddenly, our test
(that depended on that seed to know what dice would show up) would fail, and
we wouldn't know why! In this case, we may want to simply remove randomness
completely by mocking in an alternate version of the `random.random` function.
For example, here's a version where we always return the random value 0.5
(which will mean each die has the value 6*0.5+1 = 4):

```python
    @mock.patch('random.random')
    def test_create_dice(self, random_mock):
        """Check that the resulting dice mock properly"""
        random_mock.return_value = 0.5
        n_dice = 5
        dice = Die.create_dice(n_dice)
        for i in range(n_dice):
            self.assertEqual(dice[i].value, 4)
```

### Simulating user input
To test in `test_runner.py` that the runner actually runs (independently of
whether it gives the right output), you may want yout test case to pretend to be
a user giving input. To do this, we will once again "mock" in functionality
using Python's `unittest.mock` submodule.

To simulate a user's input, you can use `unittest.mock.patch` to overwrite what
`input` means while the test case is running, as
[shown here](https://stackoverflow.com/questions/46222661/how-to-mock-a-user-input-in-python).
You'll probably want a sequence of inputs, which can be achieved using the
`side_effect` instead of `return_value`, like
```python
with mock.patch("builtins.input", side_effect=["input1", "input2", "input3"]):
    # do stuff
```
Each time the code in the `# do stuff` section includes a call for user
`input()`, this will replace the interactive code with just whatever the next
item on the list is: so the first input from the user will be the string input1,
the next will be input2, etc.

In practice, most production code doesn't call `input()` -- but it does call
APIs, databases, etc., and this sort of functionality can replace those network
calls with something local that's structured the same way. You could as easily
mock Die objects! Sometimes the intuition for how to set these up can be a
little convoluted, so try to look for
[examples](https://docs.python.org/3/library/unittest.mock-examples.html) if you
use mocks. However, it's worth making sure you also have some way to test that
all the pieces are working together without that mock, e.g. an integration test.

### Refactoring and tidying

It's possible that in the process of writing tests for this code, you'll realize
that there are parts of the code organization that make it hard to test. (For
example, the single class method `run` in the runner class is really hard to
break apart!) Sometimes, those are indicators of what you might want to
*refactor* your code, a.k.a. reorganize the classes, functions, logic, etc. so
it's easier to test the parts of the logic you care about. This can be much
faster than writing the test case with the code as is!

Refactoring is usually easier when you have a set of tests already. Run your
existing tests periodically to see if things are working as expected (whether
you're changing the behavior or trying to keep it constant). If you realize
there are edge cases that you didn't catch in your original test list for your
changes, you may decide to go back and add those tests. Make sure to commit
between steps, potentially pushing when you hit milestones where all tests are
passing.

It's possible you may also want to tidy the code up a bit in nonfunctional ways
(in particular, since some of the comments and strings in the game are kind of
mean.) Go for it, but *don't forget to test even these changes*...websites have
gone down because people who thought they'd only changed a string accidentally
edited something elsewhere without noticing!

## Turning it in
When you have your changes done, commit your code to GitHub and then submit the
link to your codebase to Canvas.
