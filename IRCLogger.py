#!/usr/bin/env python

import socket
import string
import signal
import sys

class IRCLogBot:

  def __init__(self, SERVER, PORT, NICKNAME, LOGCHANNEL):
    self.SERVER = SERVER
    self.PORT = PORT
    self.NICKNAME = NICKNAME
    self.LOGCHANNEL = LOGCHANNEL

    # create socket to handle commnunication
    self.IRCsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  def irc_con(self):
    'connect to server at specified port'
    print "Connecting to server..."
    self.IRCsock.connect((self.SERVER, self.PORT))

  def irc_send_command(self, command):
    self.IRCsock.send(command + '\n')

  def irc_join(self):
    print "Joining channel for logging"
    self.irc_send_command("JOIN %s" % self.LOGCHANNEL)

  def irc_login(self, nick='RHLogger', username='LogBot', hostname='ReverseHack', servername='ReverseHack', realname='RHIRCBot'):
    print "Logging in"
    self.irc_send_command("USER %s %s %s %s" % (username, hostname, servername, realname))
    self.irc_send_command("NICK %s" % nick)

  def irc_logout(self, logoutmsg = None):
    self.irc_send_command("QUIT %s" % logoutmsg)

  def start_logging(self):

    signal.signal(signal.SIGINT, self.stop_logging)

    while(1):
      data = self.IRCsock.recv(2048)
      print data
      msg = string.split(data)
      #print msg

      if msg[0] == "PING":
        self.irc_send_command("PONG %s" % msg[1])
      if msg[1] == "PRIVMSG" and msg[2] == self.LOGCHANNEL:
        self.logfile = open("/tmp/channel.log", "a+")
        self.nick_name = msg[0][:string.find(msg[0],"!")]

        message = ' '.join(msg[3:])
        self.logfile.write(string.lstrip(self.nick_name, ':') + ' -> '     + string.lstrip(message, ':') + '\n')

  def stop_logging(self, signal, frame):
    print "\nStopping logging!"
    self.irc_logout()
    sys.exit(0)


if __name__== "__main__":
    bot = IRCLogBot('irc.freenode.net', 6667, 'mks_test067', '#ubuntu-pune')
    bot.irc_con()
    bot.irc_login()
    bot.irc_join()
    bot.start_logging()

