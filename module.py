import irc
class Module:
    def __init__(self, sock):
        pass
    def getName(self):
        raise NameError("This is not a module!")
    def ping(self):
        pass
    def join(self, nuh, channel):
        pass
    def part(self, nuh, channel, reason):
        pass
    def quit(self, nuh, reason):
        pass
    def msg(self, nuh, channel, message):
        pass
    def raw(self, msg):
        pass
class Modulev2(Module):
	pass
class Modulev1(Modulev2):
    def __init__(self, sock):
        pass
    def ping(self):
        pass
    def handle(self, msg):
        pass
    def raw(self, msg):
        self.handle(msg)
    def getNUH(self, msg):
        ex=msg[0][1:]
        try:
            ex=ex.split('!')
            ex[1]=ex[1].split('@')
        except:
            pass
        
        try:
            return (ex[0], ex[1][0], ex[1][1])
        except:
            try:
                return (ex[0], ex[1][0], "")
            except:
                try:
                    return (ex[0], "", "")
                except:
                    return ("", "", "")

