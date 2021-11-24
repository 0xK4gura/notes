Setting Up Mona Config File with: `!mona config -set workingfolder c:\mona\%p`

We run the python file

![[Pasted image 20211120183554.png]](https://github.com/0xK4gura/notes/blob/678dfb49f162e23b99d32cf4440135a266ca53e1/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120183554.png)

PS: In the room, the amount of bytes the program crashed is at 2000 bytes, lets try to test it with 2400 bytes.

We can create a cyclic pattern of alphanumeric combinations with msf `locate pattern-create` `~/pattern-create -l <number_of_characters`

After sending with payload, we can observe the EIP Pointer with `!mona findmsp -distance 2400`

It is important to take note of the EIP Pointer ![[Pasted image 20211120182721.png]](https://github.com/0xK4gura/notes/blob/678dfb49f162e23b99d32cf4440135a266ca53e1/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120182721.png) 

Then we further explore the address with some characters; let's say we wanna exploit with the letter D and see what will we get in return.

![[Pasted image 20211120190455.png]](https://github.com/0xK4gura/notes/blob/678dfb49f162e23b99d32cf4440135a266ca53e1/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120190455.png)

D is equal to 44 in hex and we can see that there is 5 D in it

![[Pasted image 20211120184255.png]](https://github.com/0xK4gura/notes/blob/678dfb49f162e23b99d32cf4440135a266ca53e1/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120184255.png)

_I changed the D to B btw to look at it easier, welp_ 

![[Pasted image 20211120190920.png]](https://github.com/0xK4gura/notes/blob/678dfb49f162e23b99d32cf4440135a266ca53e1/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120190920.png)


In this picture, the pointer is after the 4 B's have been executed, so we'll take the 0x017BFA30 address

![[Pasted image 20211120191242.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120191242.png)

We have our badchars now. We can create a custom shellcode by isolating them. The badchars is \x00\x07\x08\x2e\x2f\xa0\a1

"Not all of these might be badchars! Sometimes badchars cause the next byte to get corrupted as well, or even effect the rest of the string.""

Since x07 comes after x00 , let us try to exclude it from the payload as well.

![[Pasted image 20211120193237.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120193237.png)

Our BadChars now still causes overflow, lets to exclude x2e as well.

![[Pasted image 20211120193935.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120193935.png)

So we repeat that with:-

`!mona bytearray -b "\x00\x07\..."` to set the BadChars `!mona compare -f C:\mona\oscp\bytearray.bin -a <address>` to set the comparison and evaluate the result

We would like to achieve this where it mentioned that the shellcode is not modified but still able to cause buffer overflow 

![[Pasted image 20211120202406.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120202406.png)


Basically we are replacing our payload to our the bytes presented ( the 4 'B' bytes)

Now lets set our address in reverse fashion 
![[Pasted image 20211120203502.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120203502.png)

![[Pasted image 20211120193035.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120193035.png)

![[Pasted image 20211120192801.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120192801.png)

![[Pasted image 20211120192910.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Bufferstack%20Overflow/attachments/Pasted%20image%2020211120192910.png)
