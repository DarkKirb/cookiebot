import module
import pickle
class Module(module.Modulev1):
    def __init__(self,sock):
        self.s=sock
        f=open("var/alias","rb")
        self.aliases=pickle.load(f)
        f.close()
        print("Loaded aliases")
    def ping(self):
        f=open("var/alias","wb")
        pickle.dump(self.aliases, f)
        f.close()
        print("Saved aliases")
    def getName(self):
        return "alias"
    def handle(self, msg):
        chan = msg[2]
        nick, user, host = self.getNUH(msg)
        if msg[2][0] != '#':
            chan=nick
        if msg[3] == ":!addalias":
            if msg[4] in self.aliases:
                self.s.send("PRIVMSG %s :Alias %s already exists." % (chan, msg[4]))
            else:
                self.aliases[msg[4]]=' '.join(msg[5:])
                self.s.send("PRIVMSG %s :Alias %s successfully created." % (chan, msg[4]))
        if msg[3] == ":!isalias":
            if msg[4] in self.aliases:
                self.s.send("PRIVMSG %s :%s is an alias." % (chan, msg[4]))
            else:
                self.s.send("PRIVMSG %s :%s is not an alias." %(chan, msg[4]))
        if msg[3] == ":!delalias":
            if msg[4] in self.aliases:
                del self.aliases[msg[4]]
                self.s.send("PRIVMSG %s :%s successfully deleted." % (chan, msg[4]))
            else:
                self.s.send("PRIVMSG %s :%s isn't an alias." % (chan, msg[4]))
        if msg[3] == ":!savealiases":
            self.ping()
            self.s.send("PRIVMSG %s :Aliases saved!" % (chan))
        for trigger, output in self.aliases.items():
            if msg[3] == ":!"+trigger:
                self.s.send(("PRIVMSG %s :"%(chan))+output.format(chan=chan, nick=nick, user=user, host=host))
