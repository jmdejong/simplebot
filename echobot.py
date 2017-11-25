#!/usr/bin/python2 -u

# the u option for python is neccesary for unbuffered io.
# if this is not present, you will have to call flush after each print (sys.stdout.flush())
# this might work different in other languages

"""
Very simple bot for example purposes

When run by simplebot, each channel this bot is in has its own instance of the bot
"""

import sys

# print welcome message
print "echobot joining"
# generally this is not a very good idea since you only want your bot to reply to commands
# this is just as example, and to test if this bot can post

while True:
    # read some input, so anything said in a channel this bot is in
    # if the "format" field is set in config, instead read the formatted version of that
    txt = raw_input()
    
    user, _sep, msg = txt.partition(": ")
    
    # command is everything before the first space in txt
    # text is everything after the first space
    command, _sep, text = msg.partition(" ")
    
    
    # respond to the !echo command
    if command == "!echo":
        # reply by saying back the text
        print ("~"+user+": "+text)
    
    # respont to !rollcall
    if command == "!rollcall":
        # print description of your bot
        print "echobot here. run with !echo. Will repeat everything you say after that. I am meant as example for simplebot. Other commands are !test, !rollcall, !break and !crash"
    
    if command == "!test":
        #the bot prints per line, so this is printed in two messages
        print "some line\nand some other line"
        
        # print automatically adds a newline to the end, but if you don't do this, the message won't be printed until the next message has a newline
        sys.stdout.write("hi there, please print me. ")
    
    if command == "!break":
        # break the loop to end the program
        break
    
    if command == "!crash":
        # crash the program, functionally the same as !break
        raise Exception("help, I'm crashing")

# When the program has ended (or crashed) it will be restarted the next time somebody says something
