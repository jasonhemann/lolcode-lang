echo "HAI 1.3\nVISIBLE \"hello world\"\nKTHXBYE" > program.lol
dd if=/dev/zero of=program.lol bs=1 count=0 seek=1M
lci program.lol
