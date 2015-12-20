---
layout: post
title: Notes on Install fcitx on Arch Linux
tags : [ArchLinux, Tools]
---

Fcitx is the official Chinese input method engine (IME) suggested by ArchWiki. Fcitx per se is awesome but every time I (re)install Arch Linux on my boxes, I had trouble getting fcitx works out of the box -- `pacman -Syu fcitx-im` doesn't give you a working IME. I guess the major facet making the installation and configuration so tricky is that fcitx doesn't provide an all-in-one confguration tool (though I guess for good reason), so as an user you have to manually put configuration snippets in several different places. Before you get all of them right, it won't work, which makes this process even trickier and frastrating. So, this is a short note about how to install and fcitx on Arch Linux in my case.

## Prerequisites

Before you proceed to install `fcitx`, you need to have proper fonts installed. As always, referring to ArchWiki (e.g. [this page](https://wiki.archlinux.org/index.php/Fonts#Chinese.2C_Japanese.2C_Korean.2C_Vietnamese)) can't be wrong.

## Installation

Let's assume the necessary fonts are properly installed, which can be verified by checking if your browser can render Chinese characters correctly when you go to renren.com or so on. Okay, basically there are three things to install: `fcitx` package, an IME you like (e.g. `fcitx-googlepinyin`) and various input method engines (for convenience, they can be installed as a bunble by  group `fcitx-im`). I also installed a GUI configuration tool (` fcitx-configtool`), which is not mandotary but makes my life a little bit easier.

```sh
pacman -Syu fcitx fcitx-googlepinyin fcitx-im  fcitx-configtool
```

## Configuration

You need to register those input method modules before using them. Depending on you choice of session manager, add the following lines to your desktop start up script files to register the input method modules and support xim programs. Use `.xprofile` if you are using KDM, GDM, LightDM or SDDM. Use `.xinitrc` if you are using startx or Slim.
 
 ```
 export GTK_IM_MODULE=fcitx
 export QT_IM_MODULE=fcitx
 export XMODIFIERS=@im=fcitx
 ```
 
In my case, manualy adding input methods in the `fcitx-configtool` is required to get things ready. Simply launch the GUI program and add input methods as you like and relogin.
 
 ## Usage
 
Believe it or not, figuring out how to trigger the input method consumed the most of my time in this process. I found two things counter-intuitive and very misleading. First, `fcitx` doesn't display a system tray icon in my case -- it is supposed to display an icon somewhere so I can know `fcitx` is working, BUT IT DOESN'T, even `fcitx` works just fine, there is NO system tray icon. I don't know why this happens but it's so confusing. Long story short: never try to find a system tray icon.

Instead, to trigger the input method, simply press `Crtl+Space` when the curcor stops at an input area, and a small box will appear. If so, you're good to go!

## Troubleshooting

The most adorable thing from an user's point of view is `fcitx-diagnose`. This is a small diagnose program coming with `fcitx` package, which does not only provide informative diagnosis but also quick fix tips. Whenever you're not sure if you're doing things right (e.g. when you can't find a system tray icon), just run ` fcitx-diagnose` and check out the red bold errors.







