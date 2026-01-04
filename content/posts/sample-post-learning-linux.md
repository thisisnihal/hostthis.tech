+++
date = '2025-06-16T02:50:21+05:30'
draft = false
title = 'Sample Post - Learning Linux Again!'
+++

Learning Linux Again!

# connecting using SSH
`ssh <username>@<remote>`
If you want to specify a port, add -p 0000, (replace 0000 with the desired port number, default port for ssh is 22).
remote could be the public IP or it can also be a domain name.

# copy file from local to remote
```bash
scp /localdirectory/example1.txt <username>@<remote>:<path>
```

# change permission of file
`chmod u+w example1.txt` will add the write (modify) permission to the file for the user (u).
g modifier for group permissions
o for world permissions
w for write
r for read
x for execute

# creating your ssh keys
`mkdir .ssh`, if it doesnt exists
`ssh-keygen –t rsa` it will create public and private keys
`chmod 600 .ssh/id_rsa` change private key permission to read only for root.
- copy the public key(on local) to the remote computer `scp .ssh/id_rsa.pub <username>@<remote>:`  (include colon too)
Now on server -
- append the keys to the authorized keys file `cat id_rsa.pub >> .ssh/authorized_keys`
- Change the permissions for the SSH folder to allow access: `chmod 700 .ssh`

