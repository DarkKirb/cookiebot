#serializes single bytes into unicode characters
sertable="!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃ"
desertable={}
for x in range(len(sertable)):
    desertable[sertable[x]]=x

def serialize(string):
    s=""
    for i in range(len(string)):
        s=s+sertable[string[i]]
    return s

def deserialize(string):
    s=b""
    for i in string:
        s=s+desertable[i].to_bytes(1, byteorder='little')
    return s

