import threading

from twisted.words.protocols import irc
from twisted.internet import protocol, reactor

class ChatBot(irc.IRCClient):
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)

    def signedOn(self):
        self.join(self.factory.channel)

    def privmsg(self, user, channel, msg):
        if channel == self.factory.channel:
            print("MSG: %s: %s", user.split("!", 0), msg)

    def sendChatMessages(self, messages):
        for message in messages:
            tosend = "%s: %s" % (message["from"].encode("ascii"),
                    message["body"].encode("ascii"))
            self.msg(self.factory.channel, tosend)

class ChatBotFactory(protocol.ClientFactory):
    protocol = ChatBot

    def __init__(self, channel, nickname="chatbot"):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        connector.connect();

    def clientConnectionFailed(self, connector, reason):
        print("Could not connect: %s" % reason)

    def buildProtocol(self, addr):
        self.clientbot = protocol.ClientFactory.buildProtocol(self, addr)
        return self.clientbot

    def sendChatMessages(self, messages):
        self.clientbot.sendChatMessages(messages)

class ChatExtender(object):
    def sendChatMessages(self, messages):
        sendChatMessages(messages)

cbf = None
def sendChatMessages(messages):
    cbf.sendChatMessages(messages)

def main():
    global cbf
    cbf = ChatBotFactory("#chatbot")
    reactor.connectTCP("irc.eighthbit.net", 6667, cbf)
    t = threading.Thread(target=reactor.run, name="IRC")
    t.start()
