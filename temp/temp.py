import re

command_prefix = '$'
channel = '<#735097009136074832>'
# text = "$say <#735097009136074832> Halo, ini test <#735097009136074832>"
# text = "$say {} Hello, I'm John".format(channel)
text = "$say Hello, I'm John"
# command = "say"

# grp = re.search(rf'^{re.escape(command_prefix)}(.*)', text) 
grp = re.search(rf'^{re.escape(command_prefix)}(?P<command>\S*)\s*(?P<the_rest>.*)', text) 
# command = grp.groups()[0].lower()
# print(command)
# print(len(command))
print(grp)
# print(grp.groupdict())
command = grp['command'].lower()
the_rest = grp['the_rest']
print(the_rest)
if the_rest == '':
    print('No manual docs\n---Program stop---')
    exit()
# print(command)
# print(the_rest)
# if '<#' in the_rest:
# the_channel = re.search(rf'(?P<the_channel><#[0-9]+>)', the_rest).groupdict()['the_channel']
the_channel = re.search(rf'(?P<the_channel><#[0-9]+>)', the_rest)
if the_channel != None:
    the_channel = the_channel.groupdict()['the_channel']
    new_text = re.search(rf'{re.escape(the_channel)}*\s*(?P<the_rest_of_say>.*)', the_rest).groupdict()['the_rest_of_say']
# the_channel = re.search(rf'(?P<the_channel><#[0-9]+>)', the_rest).groupdict()

# else:
#     print('---Program stop---')
#     exit()
print(the_channel)
try:
    print(new_text)
except:
    pass
