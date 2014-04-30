#!/usr/bin/python

import os
import sys
import re
import ConfigParser
import subprocess

def main(config):
  if len(sys.argv) == 1:
    print 'No action specified'
    exit(1)
  elif sys.argv[1] == 'stop':
    stop(config)
  elif sys.argv[1] == 'kill':
    kill(config)
  elif sys.argv[1] == 'start':
    start(config)
  elif sys.argv[1] == 'restart':
    restart(config)

def stop(config):
  print 'Stopping container ' + config.get('default', 'container name')
  subprocess.call(['sudo', 'docker', 'stop', config.get('default', 'container name')])

def kill(config):
  stop(config)
  print 'Removing container ' + config.get('default', 'container name')
  subprocess.call(['sudo', 'docker', 'rm', config.get('default', 'container name')])

def restart(config):
  kill(config)
  start(config)

def start(config):
  # print 'Restarting dnsmasq'
  # subprocess.call(['sudo', '/etc/init.d/dnsmasq', 'restart'])
  # print 'Fixing permissions'
  # subprocess.call(['sudo', 'chmod', '0777', 'logs', '-Rf'])
  # print 'Generating site config files'
  # subprocess.call(['scripts/containerinfo.py'])
  print 'Running container %s' % (config.get('default', 'container name'), )
  # TODO: Put these in a settings file.
  call_parameters = ['sudo', 'docker', 'run']
  detached = config.getboolean('default', 'detached')
  if detached:
    call_parameters.append('-d')

  for vol in config.items('volumes'):
    call_parameters.append('-v')
    call_parameters.append(vol[1].replace('%(dir)', os.getcwd()) + ':' + vol[0].replace('%(dir)', os.getcwd()))

  call_parameters.append('-name')
  call_parameters.append(config.get('default', 'container name'))
  call_parameters.append(config.get('default', 'image name'))
  # print call_parameters
  subprocess.call(call_parameters)

  web_proxy_name = config.get('default', 'proxy')
  print 'Restarting container %s' % (web_proxy_name, )
  subprocess.call(['sudo', 'docker', 'restart', web_proxy_name])



if __name__ == '__main__':
  current_folder_path, current_folder_name = os.path.split(os.getcwd())
  config = ConfigParser.RawConfigParser()
  config.read(current_folder_path + '/' + current_folder_name + '/docker-loader.conf')

  main(config)

