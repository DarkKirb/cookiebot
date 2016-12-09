#!/usr/bin/env python3
from irc import IRC
import config
import module
import imp
import sys
import traceback
sock=IRC()
msg=sock.recv()
while msg[1]!="376":
    msg=sock.recv()
sock.send("MODE %s +B" % config.nick)
sock.send("JOIN #cookiebot")
sock.send("PRIVMSG #cookiebot :Hi!")
mods=[]
for m in config.modules:
    mod=imp.load_source(m+".py", "modules/"+m+".py")
    mods.append(mod.Module(sock))
    del mod
while True:
    msg=sock.recv()
    if msg[0] == "PING":
        sock.send("PONG %s"%msg[1])
        for m in mods:
            m.ping()
        continue
    if ":darklink!" in msg[0]:
        try:
            if msg[3] == ":!quit" and msg[2] == "cookiebot":
                sock.send("QUIT")
        except:
            pass
        if(len(msg) < 4):
            continue
        if msg[3] == ":!load":
            mod=imp.load_source(msg[4]+".py", "modules/"+msg[4]+".py")
            mods.append(mod.Module(sock))
            del mod
        if msg[3] == ":!reload":
            i=0
            for m in mods[:]:
                if m.getName()==msg[4]:
                    del mods[i]
                    mod=imp.load_source(msg[4]+".py", "modules/"+msg[4]+".py")
                    mods.append(mod.Module(sock))
                i=i+1
        if msg[3] == ":!unload":
            i=0
            for m in mods[:]:
                if m.getName()==msg[4]:
                    del mods[i]
                i=i+1
    for m in mods:
        try:
            m.handle(msg)
        except Exception as exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback)
            #sock.send("PRIVMSG *schat :chat darklink")
#            sock.send("PRIVMSG darklink :Got a '%s' while handling the line '%s' with module '%s'. Please see my logs." % (repr(exception), ' '.join(msg), m.getName()))
#            sock.send("PRIVMSG darklink :Traceback: %s" %(repr(traceback.format_exception(exc_type, exc_value, exc_traceback))))
            #sock.send("PRIVMSG *schat :close darklink")


