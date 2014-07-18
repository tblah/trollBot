#!/usr/bin/python2

# This code is licenced as GPL v3. See the LICENCE file.

import re	# regular expressions
import yaml	# yaml parser

# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl
from twisted.python import log

class trollBot(irc.IRCClient):
    # IRC bot for making automated replies
    def __init__(self, nickname):
    	self.nickname = nickname
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print "Connected"		

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        print "Connection Lost"

    # twisted callbacks:
    def signedOn(self):
        self.join(self.factory.channel)

    def joined(self, channel):
        print "Joined %s" % channel

    def privmsg(self, user, channel, msg):			###### THIS IS THE INTERESTING ONE!
        # got a message
        for regex in config['regex']:
            match = re.search(regex, msg)
            if match:
                self.reply(channel, config['regex'][regex])

    def reply(self, channel, message):
    	# a wrapper for self.say() that makes sure we are utf-8

    	if isinstance(message, unicode):
    		message = message.encode('utf-8')

    	self.say(channel, message)


class trollBotFactory(protocol.ClientFactory):
	# Mostly boilerplate code here...
    def __init__(self, channel, nickname):
        self.channel = channel
        self.nickname = nickname

    def buildProtocol(self, addr):
        protocol = trollBot(self.nickname)
        protocol.factory = self
        return protocol

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # hardcoded filename atleast for now:
    config = yaml.load(open("trollBot.yaml"))
    nickname = config['irc']['nickname']
    port = config['irc']['port']
    host = config['irc']['host']
    channel  = config['irc']['channel']

    # Create factory
    factory = trollBotFactory(channel, nickname)

    # magic
    reactor.connectSSL(host, port, factory, ssl.ClientContextFactory())

    # Go!
    reactor.run()
