
"""
 *  Copyright (C) 2010, Michael "Svedrin" Ziegler <diese-addy@funzt-halt.net>
 *
 *  Mumble-Django is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This package is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
"""

from fastapi import FastAPI
from mumble.mctl import MumbleCtlBase
import os

ip = os.getenv("MUMBLE_SERVER")
port = os.getenv("ICE_PORT")
sliceFile = os.getenv("SLICEFILE")
# This is the default Mumur setting, insert your settings or leave as default 
connstring = 'Meta:tcp -h ' + str(ip) + ' -p ' + str(port)
# sliceFile  = '/usr/share/slice/Murmur.ice'
icesecret = None
print(connstring)


ctl = MumbleCtlBase.newInstance( connstring, sliceFile, icesecret )

app = FastAPI()

def getUser(user):
    fields = ["channel", "deaf", "mute", "name", "selfDeaf", "selfMute",
        "session", "suppress", "userid", "idlesecs", "recording", "comment",
        "prioritySpeaker"]
    return dict(list(zip(fields, [getattr(user, field) for field in fields])))

def getChannel(channel):
    fields = ["id", "name", "parent", "links", "description", "temporary", "position"]
    data = dict(list(zip(fields, [getattr(channel.c, field) for field in fields])))
    data['channels'] = [ getChannel(subchan) for subchan in channel.children ]
    data['users']    = [ getUser(user) for user in channel.users ]
    return data

# Display only the users connected to the server. useful when used as a widget in Android
@app.get('/widget')
async def getUsrs():
    name = ctl.getConf(1, "registername")
    tree = ctl.getTree(1)

    serv = {
        'id':   1,
        'name': name,
        'root': getChannel(tree)
        }

    rawdata = serv
    data = rawdata['root']['channels']
    userlist = []
    for channel in data:
        usersinfo = channel['users']
        for userinfo in usersinfo:
            name = userinfo['name']
            userlist.append(name)
    return {"Online Users:" : userlist}


@app.get('/{srv_id}')
async def getTree(srv_id:int):
    name = ctl.getConf(srv_id, "registername")
    tree = ctl.getTree(srv_id)

    serv = {
        'id':   srv_id,
        'name': name,
        'root': getChannel(tree)
        }

    return serv

@app.get('/')
async def getServers():
    servers=ctl.getBootedServers()
    return servers

