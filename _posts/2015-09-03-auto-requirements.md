---
layout: post
tags: ["Python", "dev"]
title: "Automatically generate requirements file for Python project"
---

When you need to move your Python project around, say, to test under the
production environment, or to run a heavy load script on your powerful cloud
rack, you would better duplicate the exact development environment to avoid
compatibility issues.

My practice for doing this migration is to use `pip` as package management
tool and use `requirements.txt` file to document dependencies. Then, to
recover the exact python environment, I just

    pip install --user -r requirements.txt

Note that `--user` is used so `sudo` is not required.
If `virtualenv` is used, probably `--user` is not necessary neither.
But mostly I find `virtualenv` actually an overkill and just use vanilla
pip instead. I use `--user` so as pip will not mess up with default packages
installed by Mac OS (on the othe hand, `--system` will).

Another tool I find useful in automating this process is `pipreqs`, which
can analyze `import` in your project and extract them into
requirements files.

    pip install pipreqs
    pipreqs /path/to/project

For completeness, another tangentially relevant choice is `pip freeze`,
which lists all installed packages on your machine (you can filter items
by appending `--user` and/or other filters to `freeze` command), but maybe
not all of them are used in your project.
ear
