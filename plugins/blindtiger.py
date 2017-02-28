from __future__ import unicode_literals
import json
import time
from time import gmtime, strftime
import socket

from rtmbot.core import Plugin, Job

import click
help_text="""
  Rowr! You can say:
  `@blind.tiger please open the blind` | :full_moon:
  `@blind.tiger please close the blind` | :new_moon:
  `@blind.tiger stop` | :stop:
      """
def do_open():
  click.click(2)

def do_close():
  click.click(1)

def say(slack_client, channel, text):
  slack_client.api_call(
    "chat.meMessage", channel=channel, text=text)

def my_channels(slack_client):
  ret = list()
  r = slack_client.api_call("channels.list", exclude_archived=True)
  if r.get('ok'):
    for c in r['channels']:
      if c['is_member']:
        ret.append(c['id'])
  r = slack_client.api_call("groups.list", exclude_archived=True)
  if r.get('ok'):
    for g in r['groups']:
      ret.append(g['id'])
  return ret

def broadcast(slack_client, message):
  for c in my_channels(slack_client):
    say(slack_client, c, message)

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    return s.getsockname()[0]

class Morning(Job):
  def run(self, slack_client):
    if strftime("%H %M", gmtime()) == '13 00':
      do_open()
      return [ [x , "Rawr! Good Morning! Time to open the blinds!"] for x in my_channels(slack_client) ]
    return []
    
class BlindTiger(Plugin):

  def __init__(self, name=None, slack_client=None, plugin_config=None):
    super(BlindTiger, self).__init__(name, slack_client, plugin_config)
    self.version = 'v0.1b'
    click.init()
    self.my_id = plugin_config['bot_id']
    self.stale_seconds = plugin_config.get('stale_seconds', 5.0)
    self.atme = '<@{}>'.format(self.my_id)
    self.funcs = {
      # opens
      self.atme + ' please open the blind'  : self.open_blind,
      ':full_moon'                          : self.open_blind,
      ':sun'                                : self.open_blind,

      # closes
      self.atme + ' please close the blind' : self.close_blind, 
      ':new_moon'                           : self.close_blind, 

      # stops
      self.atme + ' stop'                   : self.stop_blind,
      ':stop:'                              : self.stop_blind,

      # other
      self.atme + ' help'                   : self.show_help,
      self.atme + ' open the pod bay doors' : self.jokes,
    }
    broadcast(slack_client, 
      "Rowr! Blind tiger %s online from %s.\n%s" % (
        self.version, str(getNetworkIp()), help_text))
    self.last_op = None
    
  def register_jobs(self):
    job = Morning(60)
    self.jobs.append(job)

  def catch_all(self, data):
    #print json.dumps(data, indent=4)
    pass
  
  def process_message(self, data):
    if (time.time() - float(data['ts'])) > self.stale_seconds:
      return
    for k, v in self.funcs.iteritems():
      if data['text'].startswith(k):
        v(data)
        break;
    else:
      if data['text'].startswith(self.atme):
        self.show_help(data)

  def stop_blind(self, data):
    if self.last_op == 'open':
      do_open()
    else:
      do_close()
    self.outputs.append([
      data['channel'],
      "Rowr?!"
    ])

  def open_blind(self, data):
    do_open()
    self.last_op = 'open'
    self.outputs.append([
      data['channel'],
      "Rowr rowr!"
    ])

  def close_blind(self, data):
    do_close()
    self.last_op = 'close'
    self.outputs.append([
      data['channel'],
      "Rowr rowr rowr!"
    ])
  
  def show_help(self, data):
    self.outputs.append([
      data['channel'],
      help_text
    ])

  def jokes(self, data):
    self.outputs.append([
      data['channel'],
      "Sorry <@%s>, I can't do that" % data['user'],
    ])


