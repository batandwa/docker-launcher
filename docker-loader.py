#!/usr/bin/python

import os
import sys
import re
import subprocess

def main(container_name):
  if len(sys.argv) == 1:
    print 'No action specified'
    exit(1)
  elif sys.argv[1] == 'stop':
    stop(container_name)
  elif sys.argv[1] == 'kill':
    kill(container_name)
  elif sys.argv[1] == 'start':
    start(container_name)
  elif sys.argv[1] == 'restart':
    restart(container_name)

def stop(container_name):
  print 'Stopping container ' + container_name
  subprocess.call(['sudo', 'docker', 'stop', container_name])

def kill(container_name):
  stop(container_name)
  print 'Removing container ' + container_name
  subprocess.call(['sudo', 'docker', 'rm', container_name])

def restart(container_name):
  kill(container_name)
  start(container_name)

def start(container_name):
  # print 'Restarting dnsmasq'
  # subprocess.call(['sudo', '/etc/init.d/dnsmasq', 'restart'])
  # print 'Fixing permissions'
  # subprocess.call(['sudo', 'chmod', '0777', 'logs', '-Rf'])
  # print 'Generating site config files'
  # subprocess.call(['scripts/containerinfo.py'])
  print 'Running container %s' % (container_name, )
  # TODO: Put these in a settings file.
  subprocess.call(['sudo', 'docker', 'run', '-d', '-v', current_folder_path + '/' + current_folder_name + ':/docker', '-v', '' + current_folder_path + '/' + current_folder_name + '/mysql:/var/lib/mysql', '-v', '' + current_folder_path + '/' + current_folder_name + '/site:/var/www', '-name', container_name, 'fjmk/docker-drupal-dev'])

  web_proxy_name = 'web-proxy'
  print 'Restarting container %s' % (web_proxy_name, )
  subprocess.call(['sudo', 'docker', 'restart', web_proxy_name])



if __name__ == '__main__':
  current_folder_path, current_folder_name = os.path.split(os.getcwd())
  config = ConfigParser
  container_name = re.sub(r'[^a-zA-Z\-_ ]', '', current_folder_name.lower()).replace(' ', '-').replace('--', '-')
  main(container_name)

