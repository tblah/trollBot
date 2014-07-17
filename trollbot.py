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
        linuxRegex = '(\s|^)[lL]inux'
        ossRegex = '[oO]pen\s[sS]ource'

        matches = re.search(linuxRegex, msg)
        if matches:
            self.reply(channel, "I would like to interject for a moment. What you're refering to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX.\n\nMany computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called 'Linux', and many of its users are not aware that it is basically the GNU system, developed by the GNU Project.\n\nThere really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called 'Linux' distributions are really distributions of GNU/Linux.")

        matches = re.search(ossRegex, msg)
        if matches:
            self.reply(channel, "It looks like you need to read https://gnu.org/philosophy/open-source-misses-the-point.html. Open source is a development model, saying this is does not recomend the political importance of Free Software.")

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