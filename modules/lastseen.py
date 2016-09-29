import module
import pickle
import time
class Module(module.Modulev1):
    def __init__(self,sock):
        self.s=sock
        f=open("var/lastseen","rb")
        try:
            self.lastseen=pickle.load(f)
        except:
            self.lastseen={}
        f.close()
    def getName(self):
        return "lastseen"
    def ping(self):
        f=open("var/lastseen", "wb")
        pickle.dump(self.lastseen, f)
        f.close()
    def handle(self, msg):
        chan = msg[2]
        nick, user, host = self.getNUH(msg)
        if msg[2][0] != '#':
            chan=nick
        self.lastseen[nick] = (int(time.time()), msg)
        if msg[3] == ':!save':
            self.ping()
        if msg[3] == ':!seen':
            if msg[4] in self.lastseen:
                tim,mesg=self.lastseen[msg[4]]
                ago=int(time.time())-tim
                if mesg[1]=="JOIN":
                    self.s.send("PRIVMSG %s :%s joined %s %s seconds ago." % (chan, msg[4], mesg[2][1:], ago))
                elif mesg[1]=="PART":
                    self.s.send("PRIVMSG %s :%s left %s %s seconds ago with reason: %s" % (chan, msg[4], mesg[2], ago, (' '.join(mesg[3:]))[1:]))
                elif mesg[1]=="QUIT":
                    self.s.send("PRIVMSG %s :%s quit %s seconds ago with reason: %s" % (chan, msg[4], ago,  (' '.join(mesg[2:]))[1:]))
                else:
                    self.s.send("PRIVMSG %s :%s was last seen %s seconds ago in %s saying: %s" % (chan, msg[4], ago, mesg[2], (' '.join(mesg[3:]))[1:]))
            else:
                self.s.send("PRIVMSG %s :Who is %s?" % (chan, msg[4]))
