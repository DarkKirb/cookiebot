import config
from passgen import keyscrambler
import socket
class IRC:
    def __init__(self):
        self.password=config.password
        self.pendingLines=[]
        self.partialLine=""
        if config.genpassword:
            self.password=keyscrambler.genpassword(self.password, "cookiebot")
        if config.znc:
            self.password=config.nick+"/"+config.networkname+":"+self.password
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((config.server, config.port))
        if len(self.password):
            self.send("PASS %s" % self.password)
        self.send("NICK %s" % config.nick)
        self.send("USER %s %s %s :%s" % (config.username, config.username, config.username, "Cookiebot"))
        while True:
            msg=self.recv()
            if msg[1] == "001":
                print("Connected to network!")
                break

    def recv(self):
        if len(self.pendingLines):
            msg=self.pendingLines.pop(0)
            print("s>c " + msg)
            return msg.split(' ')
        msga = self.s.recv(65536)
        try:
            msg = msga.decode("UTF-8")
        except:
            #Fail! Encoding wrong! Let's bother the user to switch to UTf-8
            msg = msga.decode("ISO-8859-1").split(' ')
            self.send("PRIVMSG %s :%s: Can you please set your encoding to UTF-8? I can't understand what you're saying as long as you use a legacy encoding." % (msg[2], msg[0]))
            msg = ""
        msgs = msg.split('\r\n')
        msg=""
        for i in range(1,len(msgs)-1):
            self.pendingLines.append(msgs[i])
        if len(self.partialLine):
            msg = self.partialLine + msgs[0]
            self.partialLine=""
        if msgs[len(msgs)-1] != "":
            self.partialLine = msgs[len(msgs)-1]
            msgs[len(msgs)-1]=""
        if msg!="":
            print("s>c " + msg)
            return msg
        print("s>c " + msgs[0])
        return msgs[0].split(' ')

    def send(self, msg):
        out=msg
        if not isinstance(msg, str):
            out=' '.join(msg)
        print("s<c " + msg)
        self.s.sendall((msg+"\r\n").encode("UTF-8"))
    def privmsg(self, chan, msg):
        send("PRIVMSG %s :%s" % (chan,msg))
    def join(self, chan, key=None):
        if key == None:
            send("JOIN %s" % (chan))
        else:
            send("JOIN %s %s" % (chan,key))
    def part(self, chan, reason="Parting..."):
        send("PART %s :%s" % (chan, reason))
    
