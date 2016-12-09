import module
from libs import bin2unicode
from libs import chacha
import hashlib
import array
def encrypt(msg4, data):
    keyiv=hashlib.sha512(msg4.encode("UTF-8")).digest()
    key=keyiv[:32]
    iv=keyiv[32:]
    ctx=chacha.keysetup(iv,key)
    c=chacha.encrypt_bytes(ctx, data, len(data))
    return c

class Module(module.Modulev1):
    def __init__(self,sock):
        self.s=sock
    def getName(self):
        return "say"
    def handle(self, msg):
        chan = msg[2]
        nick, user, host = self.getNUH(msg)
        if msg[2][0] != '#':
            chan=nick
        if msg[3]==":!encrypt":
            out=encrypt(msg[4], (str.join(' ',msg[5:])).encode("UTF-8"))
            self.s.send("PRIVMSG {chan} :{msg}".format(chan=chan, msg=bin2unicode.serialize(out)))
        if msg[3]==":!decrypt":
            out=encrypt(msg[4], bin2unicode.deserialize(str.join(' ',msg[5:])))
            out=array.array('B', out).tostring()
            self.s.send("PRIVMSG {chan} :{msg}".format(chan=chan, msg=out.decode("UTF-8")))
