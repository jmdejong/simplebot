#!/usr/bin/python3

import irc.bot
import json
from subapi import SubApi
import time
import sys
from ircsender import IrcSender
import os
import os.path

class SimpleBot(irc.bot.SingleServerIRCBot):
    
    def __init__(self, program, channels, nickname, server='localhost', port=6667, format=None):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        
        self.program_arguments = program
        self.game_sessions = {}
        self.chanlist = channels
        self.lastMsg = time.time()
        self.format = format
        if self.format == None:
            self.format = "{message}"
        
        self.sender = IrcSender()
    
    def on_welcome(self, c, e):
        self.connection = c
        
        self.sender.setConnection(c)
        
        for channel in self.chanlist:
            c.join(channel)
    
    
    def on_join(self, c, e):
        if e.source.nick != c.get_nickname():
            return
        chan = e.target
        gameSession = SubApi()
        gameSession.outputListeners.add(lambda text: self.send_message(chan, text))
        gameSession.start(self.program_arguments)
        self.game_sessions[chan] = gameSession
    
    def on_pubmsg(self, c, e):
        self.process_command(c, e, e.arguments[0])

    def on_privmsg(self, c, e):
        self.process_command(c, e, e.arguments[0])

    def process_command(self, c, e, text):
        sender = e.source.nick
        chan = e.target
        message = self.format.format(
            text = text,
            message = text,
            nick = sender,
            name = sender,
            sender = sender,
            chan = chan,
            channel = chan
            )
        self.game_sessions[chan].sendInput(message)
        
    # send a message
    # use ircsender to wrap messages and prevent flooding
    def send_message(self, chan, text):
        self.sender.send(chan, text)
    
    # when sending too many messages in a shot time a flooding error will occur, disconnecting the bot
    # this code makes sure at least half a second is between sending of messages
    def _waitForMessage(self):
        while(time.time() - self.lastMsg < 0.5):
            time.sleep(0.2)
        self.lastMsg = time.time()



if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path) as f:
        config = json.load(f)
    os.chdir(os.path.dirname(config_path)) # make sure all paths in config are relative to directory of config.json
    bot = SimpleBot(config["program"], config["channels"], config["nickname"], config["server"], config["port"], config["format"])
    bot.start()
