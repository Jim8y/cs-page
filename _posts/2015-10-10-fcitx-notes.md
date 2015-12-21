---
layout: post
title: Installing fcitx (a Chinese IME) on Arch Linux
tags : [Arch Linux, Tools]
---

Fcitx is a popular Chinese input method engine (IME) suggested by ArchWiki.
Fcitx is awesome but every time I (re)install Arch Linux on my boxes, I had
trouble getting fcitx works out of the box -- `pacman -Syu fcitx-im` doesn't
give you a working IME. I guess a major facet making the installation and
configuration so tricky is that fcitx doesn't provide an all-in-one configuration
tool (I guess for good reason though), so as an user you will have to manually
put various configuration snippets at several different places. Before getting
all of them right, fcitx won't work, which makes this process frustrating.
So, this short note serves as a memo for myself and hopefully will help others 
run into the similar troubles. 

# Prerequisites

Before you proceed to install `fcitx`, you need to have proper fonts installed.
As always, referring to ArchWiki (e.g. [this page][1]) can't be wrong.

# Installation

Let's assume the necessary fonts have been properly installed, which can be
verified by checking if your browser can render Chinese characters correctly
when you go to renren.com or so on. 

Okay, basically there are three pieces of software to be installed: the `fcitx`
itself, one or more IMEs of your choices (e.g. I like `fcitx-googlepinyin`)
and a couple of input method engines for various toolkits (gtk2, gtk3, etc.).
For convenience, they can be installed as a bundle by  group `fcitx-im`. I also
installed a GUI configuration tool (` fcitx-configtool`), which is not mandatory
but makes my life a little bit easier.

```shell
pacman -Syu fcitx fcitx-googlepinyin fcitx-im  fcitx-configtool
```

# Configuration

As I said, there are multiple pieces of configuration to be tweaked. Before
getting all of them right, fcitx will not work.

First, you need to register
those input method modules before using them. Depending on you choice of
display 
manager, add the following lines to your startup script file to. Use `.xprofile` if
you are using KDM, GDM, LightDM or SDDM. Use `.xinitrc` if you are using `startx`
or Slim.
 
 ```shell
# .xprofile or .xinitrc
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS=@im=fcitx
 ```
 
Second, if your locale is `en_US.UTF-8`, IME for Chinese will *not* be activated
by default. You'll get a notice by `fcitx-dianose` command like this:

```
## Input Methods:
	1.  Found 1 enabled input methods:
			fcitx-keyboard-us
	2.  Default input methods:
		**You only have one input method enabled, please add a keyboard input method as the first one and your main input method as the second one.**
```

In my case, I managed to add `google-pinyin` using `fcitx-configtool`. Simply
launch the GUI program and add input methods as you like and re-login.
 
# Use fcitx
 
Believe it or not, figuring out how to switch to Chinese input mode
consumed the most of my time in this process. One correct way of doing 
this is to press `Ctrl-Space` while focusing on an input field.
If a little widget shows up, you're all set. Otherwise, which is highly
likely, please proceed to the next section :)

# Troubleshooting

Fcitx provided nice tools for troubleshooting. However, before getting to the
correct way of debugging, please be advised not to fall into the following
pitfall as I did:

If you're using a desktop environment that happens to a system tray, don't
expect an icon there for fcitx (although many other IMEs do have system tray
icons). For unknown reasons, `fcitx` doesn't display a system tray icon in my
case, which confused me a lot because I expect that icon to appear to indicate
fcitx is working properly. Long story short: never try to find a system tray
icon.

The most adorable thing from an user's point of view is `fcitx-diagnose`. This
is a small diagnose program coming with `fcitx` package, which does not only
provide informative diagnosis but also quick fix tips. Whenever you're not sure
if you're doing things right (e.g. when you can't find a system tray icon),
just run ` fcitx-diagnose` and check out the red bold errors.

# Resources

I found ArchWiki page on [fcitx][2] super informative.


[1]:https://wiki.archlinux.org/index.php/Fonts#Chinese.2C_Japanese.2C_Korean.2C_Vietnamese
[2]:https://wiki.archlinux.org/index.php/Fcitx


