#!/usr/bin/env python

import socket
import string
import signal
import sys
from time import gmtime, strftime
from datetime import datetime
from dateutil import tz



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

  def irc_login(self, username='LogBot', hostname='ReverseHack', servername='ReverseHack', realname='RHIRCBot'):
    print "Logging in"
    self.irc_send_command("USER %s %s %s %s" % (username, hostname, servername, realname))
    self.irc_send_command("NICK %s" % self.NICKNAME)

  def irc_logout(self, logoutmsg = None):
    self.irc_send_command("QUIT %s" % logoutmsg)

  def start_logging(self):

    # Register Ctrl+C handler so that we can gracefully logout
    signal.signal(signal.SIGINT, self.stop_logging)

    while(1):
      data = self.IRCsock.recv(2048)
      print data
      msg = string.split(data)
      #print msg

      # Handle Alive state
      if msg[0] == "PING":
        self.irc_send_command("PONG %s" % msg[1])

      # Handle private messages to bot
      if ('PRIVMSG' == msg[1]  and self.NICKNAME == msg[2] ) or ('PRIVMSG' == msg[1] and self.LOGCHANNEL == msg[2] and self.NICKNAME == string.strip(msg[3], ':,')):
        self.nick_name = string.lstrip(msg[0][:string.find(msg[0],"!")], ':')
        self.privmsg = ":Heya there! I'm LoggerBot, Do Not Disturb Me!"
        self.irc_send_command("PRIVMSG %s %s" % (self.nick_name, self.privmsg))

      # Actual logging of channel
      if msg[1] == "PRIVMSG" and msg[2] == self.LOGCHANNEL:
        self.logfile = open("/tmp/channel.log", "a+")
        self.nick_name = msg[0][:string.find(msg[0],"!")]

        timenow = self.convert_utc2local(strftime("%Y-%m-%d %H:%M:%S", gmtime()), 'Asia/Kolkata')
        message = ' '.join(msg[3:])
        self.logfile.write(timenow + " " + string.lstrip(self.nick_name, ':') + ' -> '     + string.lstrip(message, ':') + '\n')
        self.logfile.flush()

  def convert_utc2local(self, time2convert, convert2):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(convert2)

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc = datetime.strptime(time2convert, '%Y-%m-%d %H:%M:%S')

    utc = utc.replace(tzinfo=from_zone)

    central = utc.astimezone(to_zone)
    timenow = central.isoformat()[:10] + " " + central.isoformat()[11:-6]
    return timenow


  def stop_logging(self, signal, frame):
    print "\nStopping logging!"
    self.irc_logout()
    sys.exit(0)

