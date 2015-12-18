---
layout: post
title : "Quotation concept in Unix Shell"
tages : ["Shell"]
---

Tell me how to quote.

The basic actions of the shell are simple. It reads a line. This is
either from a file, a script, or from a user.

- First, meta-characters are "handled."
- Second, the name of the executable is found.
- Third, the arguments are passed to the program.
- Fourth, the file redirection is setup.
- Lastly, the program is executed.

Meta-characters and Filename expansion
--------------------------------------

This includes **variable evaluation** (variables start with a `$`), and
**filename expansion**.

Quotation
---------

Why quote at all, and what do I mean by quoting? Well, the shell
understands many special characters, called `meta-characters`. These
each have a purpose, and there are so many, beginners often suffer from
meta-itis. Example: The dollar sign(`$`) is a meta-character, and tells
the shell the next word is a variable. If you wanted to use the dollar
sign as a regular character, how can you tell the shell the dollar sign
does not indicate a variable? Answer: the dollar sign must be
**quoted**. Why? **Quoted characters do not have a special meaning.**

> Quoted characters do not have a special meaning.

A surprising number of characters have special meanings. The lowly
space, often forgotten in many books, is an extremely important
meta-character. Consider the following


```shell
rm -i file1 file2
```

The shell breaks this line up to four words, which can be logically
divided into two classes.

1.  `rm` is program to execute
2.  `-i`, `file1`, `file2` are parameters or arguments, which will be
    passed to `rm` before it runs.

To shell, there is no difference between `-i` and `file1`, except that
it follows convention that options begin with a hyphen, like `-i`. All
shell cares is to extract four words from the line, then find the
executable `rm` and pass the other three parameters to it. However, when
you input the quoted version, it will be another story


```shell
rm -i 'file1 file2'
```

Note that, "quoted characters do not have a special meaning" , so does
the space between 'file1' and 'file2'. DO NOT perceive 'file1 file2' as
a string in C or any other programming languages. **There is no concept
of C-like string in shell** and don't even try to make the metaphor,
which is often overlooked by beginners yet extremely important to keep
in mind, in order to understand quotation correctly.

A more accurate description of the quoting is a **switch**, or toggle --
it turns on and off the quotation status whether the meta-characters
within text are getting to be interpreted. Therefore, following
variations are all equivalent

```shell
rm 'file1 file2'
rm file1' 'file2
rm f'ile1 file'2
```

Just remember: There is NO concept of string in shell at all.

Strong versus weak quoting
--------------------------

Simple enough,

-   `"` is weakest: backslash(`\`), dollar sign(`$`), and the
    back-stick(\`\`) all keep effective inside the double quotation.
-   `'` is strongest: single quotation returns everything inside the
    quotation literally.

Nested quotation
----------------

Once you have fully understood that The quotation marks in the Bourne
shell are not used to define a string, but to **disable** or **enable**
interpretation of meta-characters, it's easy and intuitive to play with
so called 'nested quotation'


```shell
$ echo 'Strong quotes use '"'"' and weak quotes use "'
Strong quotes use ' and weak quotes use "
```


Above example tells all story about nested quotation. Equivalently

```shell
$ echo '"'"'"
```


simply gives `"'`.

some tricky cases
-----------------

There are always chances for you to use nested quotation in composing a
program. What makes it tricky is that the order of quotation matters,
let's look at something live

```shell
$perl -e "print('hello world')"
hello world$
```

Printing hello world as we excepted, but Where is the \$ from? No magic,
it is the beginning of the next line, because the absence of
`line switch` at the tail of 'hello world'. You might think following is
fine

```shell
$perl -e "print('hello world\n')"
hello world\n$
```

But it isn't. Single quotation scapes 'n' as Perl string syntax
specified (NOTE, n is an escape chatachter defined by programing
language, which has nothing to do with quotation in shell). In this
cases, following is the way to set it right


```shell
$perl -e 'print("hello world\n")'
hello world
```

Another question worthy of thinking is, will
`perl -e print("hello world\n")` works? Now that `'a'` has no difference
with `a` to shell, why `'print("hello world\n")'` works while
`print("hello world\n")` doesn't? Here is the result


```shell
$perl -e print("hello world\n")
Unknown file attribute.
```


What's next
------------

I'm planning to write something about **escape character versus
quotation** later.
