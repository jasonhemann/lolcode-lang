import io
import sys

import lolcode

def test_main():
    stdin = sys.stdin
    sys.stdin = io.StringIO('1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n')
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','test.lol'])
    lolcode.lolcode(['','/dev/null'])
    lolcode.lolcode(['','first_primes.lol', '-v'])
    lolcode.lolcode(['','first_primes.lol', '-a'])

if __name__ == '__main__':
    test_main()
