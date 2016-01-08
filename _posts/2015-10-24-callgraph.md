---
layout: post
title: Generating Callgraphs from C/C++ Source Files
tags: [Programming Languages, Tools]
---

When studying the TCB size of modern cryptography implementations (e.g. HELib
and NTL for Homomorphic Encryption), I needed a tool to count lines of code that
are involved in a single run of a program.
It is actually not easy to accomplish thought it sounds like
a piece of cake.
I started with the idea of generating a function call graph and count LoC
function by function.

It turned out there are tools scattering around. This note briefly documented
the way I combined them together to generate call graphs from C/C++ source
code.

# Dump callgraphs with clang

`clang` has a nice tools `opt` that is capable of doing various optimizations
and analyses. Quoted from the [documentation][2]:

> When `-analyze` is specified, `opt` performs various analyses of the input source.

In particular, the `-dot-callgraph` option will dump the call graph to `callgraph.dot`:

```shell
clang++ -S -emit-llvm main.cpp $(CFLAGS) -o - | opt -analyze -dot-callgraph
```

# De-mangling using c++filt

Function names in the dot callgraph are mangled and not readable by human.
To de-mangle it, [`c++filt`][1] can be used:

```bash
> c++filt -n _Z1fv
f()
```

`c++filt` works with STDIN in a even more elegant way: it can intelligently
separate the mangled names from surrounding text, so the following
commands crisply de-mangle all function names:

    cat callgraph.dot | c++filt -n  > callgraph

Finally, `dot`, of course, comes handy to transform `dot` files to PDFs (and
many other formats:

    dot -Tpdf -ocallgraph.pdf callgraph

Here we go! A callgraph is generated.

# Fine-tune with networkx

If further analysis is desired, `networkx` package for Python is handy and powerful.
It can read and write `dot` files so at the end of day, one can draw the
call graph using the same `dot` command.

# Note

`binutils` can be installed by Homebrew on Mac OS,

```
brew install binutils
```

opt is in the llvm package, can you might have to link it manually
to /usr/local/bin (or anywhere in your `$PATH`)

```
ln -s /usr/local/Cellar/llvm/3.6.2/bin/opt /usr/local/bin/opt
```

[1]: https://sourceware.org/binutils/docs/binutils/c_002b_002bfilt.html
[2]: http://llvm.org/docs/CommandGuide/opt.html
