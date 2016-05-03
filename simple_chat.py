#!/usr/bin/env python
# encoding: utf-8

"""
Description
"""

__author__ = 'mohammad.rafi@inmobi.com (Mohammad Rafi)'

import cachetools
import datetime
import os
import select
import sys
import xmpp


DUPLICATE_TIMEOUT = 5


class Bot:

    def __init__(self, jabber, remotejid):
        self.jabber = jabber
        self.remotejid = remotejid
        self.cache = cachetools.TTLCache(100000, DUPLICATE_TIMEOUT)

    def register_handlers(self):
        self.jabber.RegisterHandler('message', self.xmpp_message)

    def check_duplicate_and_print(self, event):
        if self.cache.get(event.getBody()):
            sys.stdout.write('Got Duplicate \n')
        else:
            sys.stdout.write(event.getBody() + '\n')
        # FIXME: Shoulw we be adding it for duplicate messages as well?
        self.cache[event.getBody()] = True

    def xmpp_message(self, con, event):
        type = event.getType()
        fromjid = event.getFrom().getStripped()
        if type in ['message', 'chat', None] and fromjid == self.remotejid:
            self.check_duplicate_and_print(event)

    def stdio_message(self, message):
        m = xmpp.protocol.Message(to=self.remotejid, body=message, typ='chat')
        self.jabber.send(m)
        pass

    def xmpp_connect(self):
        con = self.jabber.connect()
        if not con:
            sys.stderr.write('could not connect!\n')
            return False
        sys.stderr.write('connected with %s\n' % con)
        auth = self.jabber.auth(jid.getNode(), jidparams['password'],
                resource=jid.getResource())
        if not auth:
            sys.stderr.write('could not authenticate!\n')
            return False
        sys.stderr.write('authenticated using %s\n' % auth)
        self.register_handlers()
        sys.stderr.write('Please write a message to send once.')
        return con


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Syntax: xtalk JID"
        sys.exit(0)

    tojid = sys.argv[1]

    jidparams = {}
    print 'Please wait while we establish a connection'

    jidparams['jid'] = 'foo@localhost'
    jidparams['password'] = 'foo'

    jid = xmpp.protocol.JID(jidparams['jid'])
    cl = xmpp.Client(jid.getDomain(), debug=[])

    bot = Bot(cl, tojid)

    if not bot.xmpp_connect():
        sys.stderr.write("Could not connect to server, or password mismatch!\n")
        sys.exit(1)

    cl.sendInitPresence(1)

    socketlist = {cl.Connection._sock: 'xmpp', sys.stdin: 'stdio'}
    online = 1

    while online:
        (i, o, e) = select.select(socketlist.keys(), [], [], 1)
        for each in i:
            if socketlist[each] == 'xmpp':
                cl.Process(1)
            elif socketlist[each] == 'stdio':
                msg = sys.stdin.readline().rstrip('\r\n')
                bot.stdio_message(msg)
            else:
                raise Exception("Unknown socket type: %s" % repr(socketlist[each]))
    cl.disconnect()
