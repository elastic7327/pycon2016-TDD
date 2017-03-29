#!/usr/bin/python
# -*- coding: utf-8 -*-

# from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random, os

env.hosts = [os.environ["BLOG_HOST"], ]
env.password = os.environ['BLOG_PW']
env.user = os.environ['BLOG_USER']

RESP_URL = "https://github.com/elastic7327/pycon2016-TDD.git"

def deploy():
    local('uptime')


def host_type():
    run('uname -s')


def uptime():
    run('uptime')
    # local('uptime')


def hello(who="world"):
    run('ls -alg')
