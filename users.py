# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""


# # List of features for single user ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#     1.User in List can enter
#     2.New User can also register
#     3.Sender sends messages to the client not in system-New client will be added and messages will be sent to the new user once he Registers himself
#     4.He will be able to see the messages even he is offline after login in.Messages are stored in Memory  LRU and in List
#     5.Single chat messages are stored in list with the time of its entry for feature analytics
#
#
#List of features for Group user |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#     1.User can chat to the existing group-Group 1 and group2
#     2.New group can be created with its own name and list of users.
#     3.Group messages are stored in list with the time of its entry.
#     4.Group chat messages are stored in list with the time of its entry for feature analytics
#
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

from __future__ import print_function
__all__ = [ 'ValueError', 'pad', 'unpad' ]
import sys



from Crypto.Util.py3compat import *
import yaml
import grpc
import sys
import messenger_pb2
import messenger_pb2_grpc
import re
from datetime import datetime
from Crypto.Cipher import AES
# from Crypto import Random

# from Padding import pad, unpad

# Spartan Server Port
port=0

# LRU cache
max_num_messages_per_user=0

# Rate limit
max_call_per_30_seconds_per_user=0

# 1-1 messaging
users = []

# Group messaging
groups={}
group1=[]
group2=[]


# +++++++++++++DECRYPTION LOGIC++++++++++++++++++++++++++++++++++++++
from Crypto.Cipher import AES

salt = '!%F=-?Pst970'

key = "{: <32}".format(salt).encode("utf-8")
# key=b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\XA2$\X05(\XD5\X18'
# Encryption
cipher=AES.new(key)

def pad(s):
  return s+((16-len(s)%16)*'{')

def encrypt(plaintext):
  global cipher
  return cipher.encrypt(pad(plaintext))


def decrypt(ciphertext):
  global cipher
  dec=cipher.decrypt(ciphertext).decode('utf-8')
  l=dec.count("{")
  return dec[:len(dec)-1]

# from Padding import pad, unpad
# ========================================Padding /UNPAD +++++++++++++++++++++++++__________________________



# /======================================================PADDING ENDS HERE=============================================

# from Crypto.Cipher import AES

import time
import datetime

def run():
  count=0
  retrievevaluesfromYaml()
  global port
  portlocal = 'localhost:' + str(port)


  global max_num_messages_per_user
  global max_call_per_30_seconds_per_user
  global users
  global groups
  global group1
  global group2
  channel = grpc.insecure_channel(portlocal)
  stub = messenger_pb2_grpc.GreeterStub(channel)
  print("[Spartan] Connected to Spartan Server at port 3000")
  print("[Spartan] User list: bob,charlie,eve,foo,bar,baz,qux")
  sender = input("Enter Ur name  = ")
  group3=group1+group2
  if sender not in group3:
    print("Thanks for Registering with us,Please go ahead" ,sender)
  grpSinglechat=input("Do you want to groupchat   -Type y or n  = ")
  grpSinglechat=grpSinglechat.strip()
  if grpSinglechat is not 'y' or 'n':
    print("Enter the valid option")


  # =======================group chat===================================
  if grpSinglechat is 'y':
    gslect=input("do u want to chat in existing groups or create new group type y or n =")
    if gslect is 'y':
      slctgrp=input(" Type g1 or g2 that u want to chat =")

      if slctgrp is 'g1':
        slctgrp = group1
      else:
        # print("overhearad ")
        slctgrp = group2

      # print(sender)
      # print(slctgrp)

      if sender not in slctgrp:
        print("Sorry you are not part of group")
        run()


      nw=''
      for usrs in slctgrp:
        if nw is None:
          nw=usrs
        else:
          nw=nw+","+usrs
      grpmessage = input("[" + sender + "] : ")

      response = stub.SayHelloAgain(
        messenger_pb2.HelloRequest(message1=sender, message2=nw, message3=grpmessage))

      while (response is not None):
        x4=formatMessage(response.message)
        print(group1)
        groupUsers = slctgrp
        # print(groupUsers)
        for receiverm in groupUsers:
          print("{" + receiverm + "] :" + x4)
        grpmessage = input("[" + sender + "] : ")

        response = stub.SayHelloAgain(
          messenger_pb2.HelloRequest(message1=sender, message2=nw, message3=grpmessage))



    print("Instructions :- read fully")
    print(" Make sure all the users are online or have opened in chat window before proceeeding to create a group, all users should create and join the group")
    userName=input("enter the users whom do u want to form a group from User list: bob,charlie,eve,foo,bar,baz,qux == ")
    groupname=input("Enter the group name ")
    grpmessage=input("[" +sender +"] : ")
    userName=userName+","+sender


    # ciphertext=encrypt(grpmessage)

    response=stub.SayHelloAgain(messenger_pb2.HelloRequest(message1=userName, message2=groupname, message3=grpmessage))
    count = count + 1
    a = datetime.datetime.now().minute

    while (grpmessage is not None):
      message = input("[" + sender + "] : ")
      # ciphertext = encrypt(message)
      response = stub.SayHelloAgain(
        messenger_pb2.HelloRequest(message1=userName, message2=groupname, message3=message))
      # plaintext=decrypt(response.message)
      count = count + 1
      els = response.message
      el = els[38:]
      print(el)

      x2 = el.replace("}", "")
      x3 = x2.replace("!", "")
      x4 = x3.replace("'", "")
      b = datetime.datetime.now().minute
      # print(b)

      c = b - a
      if c < (30) and count > max_call_per_30_seconds_per_user:
        print("Hi your sending too many messages with the time limit .Please control Only 3 messages/30 seconds ")
      print(userName)
      groupUsers=userName.split(',')

      for receiverm in groupUsers:
        print("{" + receiverm + "] :" + x4)

  # ======================================================group chat ends over here-------------------------------------------------


  # ========================================================== single user chat-last five messages ====================================================

  oldmessages = input("Dou you want to see the last 5 messages -Type y or n  = ")
  receiver =''
  message = ''
  if oldmessages is 'y':
    response = stub.SayHello(
      messenger_pb2.HelloRequest(message1=sender, message2=receiver, message3=message))
    lrulist=response.message

    print("[" +receiver +"] : " ,lrulist)



  # +==================================================================
  receiver = input("To whom you want to communicate = ")
  print(group3)
  if receiver is not group3:
    print("The reciever is not in our list, still you can send messages, we will send invitaion and will deliver messages once he joins")


  message=input("[" +sender +"] : ")
  # ciphertext = encrypt(message)
  # print(ciphertext)

  response = stub.SayHelloAgainsecond(messenger_pb2.HelloRequest(message1=sender, message2=receiver, message3=message))
  count=count+1
  a = datetime.datetime.now().second

  while (message is not None):
    message = input("[" + sender + "] : ")
    # ciphertext = encrypt(message)

    response = stub.SayHelloAgainsecond(
    messenger_pb2.HelloRequest(message1=sender, message2=receiver, message3=message))
    # plaintext = decrypt(response.message)
    count = count + 1
    els=response.message


    el=els[38:]

    x2 = el.replace("}", "")
    x3 = x2.replace("!", "")
    x4 = x3.replace("'", "")
    b = datetime.datetime.now().second
    # print(b)


    c=b-a
    if c<(30) and count>max_call_per_30_seconds_per_user:
      print("Hi your sending too many messages with the time limit .Please control only 3 messages/30 seconds ")

    print("{"+ receiver  +"] :"+ x4)


def formatMessage(msg):
  els = msg
  el = els[38:]
  print(el)

  x2 = el.replace("}", "")
  x3 = x2.replace("!", "")
  x4 = x3.replace("'", "")
  return x4



def retrievevaluesfromYaml():
  global port
  global max_num_messages_per_user
  global max_call_per_30_seconds_per_user
  global users
  global groups
  global group1
  global group2

  stream = open("config.yaml", "r")
  with open('config.yaml','r') as f:
    doc=yaml.load(f)
    port = doc["port"]
    max_num_messages_per_user = doc["max_num_messages_per_user"]
    max_call_per_30_seconds_per_user = doc["max_call_per_30_seconds_per_user"]
    users = doc["users"]
    groups = doc["groups"]
    group1 = doc["groups"]["group1"]
    group2 = doc["groups"]["group2"]
    # port = doc["port"]

    # print(group2)

def messageTimer(a,b):
  timefirst=a.replace(hour=0).replace(second=0)
  timeSecond = b.replace(hour=0).replace(second=0)
  return timeSecond-timefirst

if __name__ == '__main__':
    run()

