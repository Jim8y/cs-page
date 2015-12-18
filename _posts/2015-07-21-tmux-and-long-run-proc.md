---
Tags : ["Development", "Systems"]
title : "tmux and long run process"
---

This blog stems from a very simple question: why my tasks on remote server get killed
after my logging off from the ssh?

# session and jobs

From remote server's perspective, all incoming ssh connections are handled by sshd,
firstly forking a new sshd. To see how this works, simple examine the process tree rooted
at the oldest sshd.

	-bash-3.00$ ps xfo 'pid,pgid,sid,stat,tty,cmd' -p 23313
	  PID  PGID   SID STAT TT       CMD
	23313 23313 23313 Ss   ?        sshd: fanz [priv]
	23315 23313 23313 S    ?         \_ sshd: fanz@pts/4
	23316 23316 23316 Ss   pts/4         \_ -bash
	23357 23357 23316 R+   pts/4             \_ ps xfo pid,pgid,sid,stat,tty,cmd -p 23313

## What is `pts` by example

	-bash-3.00$ ll /proc/22612/fd/0
	lrwx------  1 fanz fanz 64 Jul 21 16:20 /proc/22612/fd/0 -> /dev/pts/4
	-bash-3.00$ ll /proc/22612/fd/1

## Controlling process and controlling tty

bash is the controlling process of pts4 and on the other hand, pts4 is the controlling
terminal of session group 23316.

## trace the shutting down of ssh connection

	strace -p 23316 -o 23316-log &
	exit

The most important log is actually the last line of 23316-log file, which is literrally
the last word `bash` could speak out before exitting itself and transferring control back
to the kernel, that is

	exit_group(0)

> This system call is equivalent to exit(2) except that it terminates not only the
> calling thread, but all threads in the calling process's thread group.

My guess is when ssh connection closes, sshd closes the tty file, which in turn triggers
a SIGHUP to be sent to the controlling process, `bash`, aka the session leader. Then
the whole session terminates as a result of turning off of its leader.
