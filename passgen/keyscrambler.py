import string
from passgen import sharandom
random=sharandom.SHARandom()
import hashlib
import getpass
sha256c=0
scramblec=0
genc=0
def sha512(string):
#    print("sha512()")
    sharandom.sha512c=sharandom.sha512c+1
    return hashlib.sha512(string.encode('UTF-8')).hexdigest()
def sha256(string):
#    print("sha256()")
    global sha256c
    sha256c=sha256c+1
    return hashlib.sha256(string.encode('UTF-8')).hexdigest()

def scramble(stringa, stringb, recursive=0):
#    print("scramble()")
    global scramblec
    scramblec=scramblec+1
    seed=sha512(sha256(stringa)+sha256(stringb))
#    print("    set scramble() seed")
    if not recursive:
        seed=scramble(sha256(stringa)+sha256(stringb), seed, 1)
#        print("    set scramble() seed")
    stringa=list(stringa)
    stringb=list(stringb)
    strings=stringa+stringb
    if recursive < 2:
        seed=scramble(sha512(''.join(strings)), seed, 2)
#        print("    set scramble() seed")
    random.setstate(seed)
    random.shuffle(strings)
    if not recursive == 3:
        random.shuffle(stringa)
        random.shuffle(stringb)
        seed=scramble(sha512(''.join(strings)),sha256(''.join(stringa))+sha256(''.join(stringb)), 3)
#        print("    set scramble() seed")
        random.setstate(seed)
    random.shuffle(strings)
    return ''.join(strings)

def genpassword(base, use, recursive=0):
    print("genpassword()")
    global genc
    genc=genc+1
    seed=sha512(scramble(sha512(base),sha512(use)))
    #print("    set genpassword() seed: %s"%seed)
    random.setstate(scramble(sha256(seed),sha256(sha512(seed))))
    for i in range(random.randint(1,25)):
            random.setstate(scramble(sha256(seed),sha256(sha512(seed))))
    random.setstate(scramble(sha256(seed),sha256(sha512(seed))))
    temp=list("".join(random.choice(string.digits+string.ascii_letters+string.punctuation) for _ in range(32)))
    if not recursive:
        random.setstate(scramble(sha256(seed),sha256(genpassword(''.join(temp),use,1))))
    else:
        random.setstate(scramble(sha256(seed),sha256(''.join(temp))))
    random.shuffle(temp)
    return ''.join(temp)
if __name__ == "__main__":
    login_pass = getpass.getpass("Scramble Password: ")
    use = input("Use: ")
    times = int(input("Key revolutions: "))
    for i in range(times):
        login_pass=genpassword(login_pass, use)
        use=scramble(sha512(login_pass), sha512(use))
        print("Revolution %i/%i done."%(i+1,times))
    print("Your password for is: %s" % (genpassword(login_pass,use)))
    print("sha512: %i, sha256: %i, rand: %i, scamble: %i, gen: %i"%(sharandom.sha512c,sharandom.randc,sha256c,scramblec,genc))
