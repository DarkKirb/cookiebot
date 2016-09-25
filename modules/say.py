import module
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
        if msg[3] == ":!say":
            self.s.send("PRIVMSG %s :%s" % (chan, ' '.join(msg[4:])))
        if msg[3] == ":!act":
            self.s.send("PRIVMSG %s :%sACTION %s%s" % (chan, chr(1), ' '.join(msg[4:]), chr(1)))
