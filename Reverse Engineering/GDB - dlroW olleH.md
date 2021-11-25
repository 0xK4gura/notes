In this example we gonna examine how to pop out a string from a memory using gdb.

First, let's create a simple program with C by using this code block;


```
#include <stdio.h>
void main(void)
{
	printf ("hello world!\n");
}
```


Save it as hello.c and then run gcc to compile it:

`gcc hello.c -o hello`

The first thing we need to do is to to know what kind of file it is with some proper identification. We can do it with `file`

![[Pasted image 20211125100145.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125100145.png)

Then we can run it with `strings` to get some valuable informations.

![[Pasted image 20211125100218.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125100218.png)

```
/lib64/ld-linux-x86-64.so.2
libcs.so.6
```

These both are the libraries the program used that usually stays at top. The rest are placed by the compiler.

The program uses `puts` instead of printf. This is due to the fact that the GCC did not perceive the string as a C-style formatting string which have formatter and control characters such as %d or %s in C. Long story short, the `puts` is used for non-formatted string and the opposite is true for `printf`

Now we can try to observe the program under disassembly. We can achieve this by `objdump -d hello > disassembly.asm` in which flag -d is used to disassemble.

The output of the file in AT&T syntax that we dump would look something like this:

![[Pasted image 20211125100942.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125100942.png)

The result yields in many function with a total of 15. Disassembly code usually at the `.text` section. And since this is GCC-compiled program, we can skip ahead to the `main` . For GoLang we can go straight to `main.main`

Things that we have covered so far are:
--> The file is 64 bit ELF Executable
--> It was compiled with GCC
--> It has ~20 functions
--> The code uses common Linux libvraries: `libc.so` and `ld-linux.so`
--> The `puts` command is used

### Dynamic Analysis

We can run `ltrace`, `strace` and `gdb`

#### ltrace
The ltrace output displays readable code of the activity of the program and code 13 is usually recevied as an exit.

![[Pasted image 20211125101917.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125101917.png)

There are many flags that can be useful when doing ltrace

~~~

-f : trace children (fork() and clone()) | gets PID
-i : print instruction pointer at time of library call
-S : trace system calls as well as libarary calls

~~~

![[Pasted image 20211125102434.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125102434.png)

#### strace
Like `ltrace -S`, strace can also logs system calls of the program. 

![[Pasted image 20211125102714.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125102714.png)

It logs every system call that happened starting from it was executed which is `execve`. `mmap2, mprotect, mbrk` are responsible for memory activities such as allocation, permissions and segment boundary settings. 

Deep within `puts` ; it executes a `writes` system call. The value 1 in the strace indicates STDOUT which is the handle for the console output. The second parameter is the message.

#### gdb

We can get `gdb` by installing it with 
	
	`sudo apt install gdb`
	
Then use gdb to start; 
	
	`gdb ./hello`
	
We can use `disass main` to dump the content of main function. (since I'm using pwndbg extension, it might look different)

![[Pasted image 20211125103522.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125103522.png)

Let's set a breakpoint with `b \*main`

	The asterisk symbol (\*) is used to mark an address location of a program

Then we can `run` the program and it should halt at the main function.

We can get the registers by `info registers` shown in extended registers for 32 bit and R-prefix for 64.

32 bit (EAX, ECX, EDX, EBX, EIP)
64 bit (RAX, RCX, RDX, RBX, RIP)

We can step into (`stepi` or `si`) and step over (`nexti` or `ni`)along with` info registers` and `disass` to navigate.

Keep entering until we reached `<puts@plt>`

![[Pasted image 20211125104420.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125104420.png)

Now, before the `puts` function gets called, we can inspect the values that were pushed into the stack with this command;

	x/8x $rsp
	
In our case, we can try to dump the content of the address that is `lea` before it gets called by `<puts@plt>`

![[Pasted image 20211125105341.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125105341.png)

When we step over (`ni`), there will be an output.

![[Pasted image 20211125105539.png]](https://github.com/0xK4gura/notes/blob/main/Reverse%20Engineering/attachments/Pasted%20image%2020211125105539.png)

