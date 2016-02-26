#!/usr/bin/env python

import mido
import time
import ConfigParser # this is version 2.x specific, on version 3.x it is called "configparser" and has a different API
import redis
import serial
import sys
import os

if hasattr(sys, 'frozen'):
    basis = sys.executable
else:
    basis = sys.argv[0]
installed_folder = os.path.split(basis)[0]

config = ConfigParser.ConfigParser()
config.read(os.path.join(installed_folder, 'volcabass.ini'))

r = redis.StrictRedis(host=config.get('redis','hostname'), port=config.getint('redis','port'), db=0)
try:
    response = r.client_list()
except redis.ConnectionError:
    print "Error: cannot connect to redis server"
    exit()

# this is only for debugging
print('-------------------------')
for port in mido.get_output_names():
  print(port)
print('-------------------------')

port = mido.open_output(config.get('midi','device'))

control_name = ['slide_time', 'expression', 'octave', 'lfo_rate', 'lfo_int', 'vco_pitch1', 'vco_pitch2', 'vco_pitch3', 'attack', 'decay_release', 'cutoff_intensity', 'gate_time']
control_cmd = [5, 11, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]

while True:
    time.sleep(config.getfloat('general', 'delay'))

    for name, cmd in zip(control_name, control_cmd):
        try:
            config.get('output', name)
            # commenting it out means that the control is to be skipped
            val = r.get(config.get('output', name))
            if val:
                val = int(val)
            else:
                val = config.getint('default', name)
            msg = mido.Message('control_change', control=cmd, value=int(val))
            print cmd, val
            port.send(msg)
        except:
            pass
