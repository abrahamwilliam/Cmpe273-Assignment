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
"""The Python implementation of the GRPC helloworld.Greeter server."""
from __future__ import print_function
from concurrent import futures
import time
import yaml



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

#
from Crypto.Util.py3compat import *

import grpc
import messenger_pb2
import messenger_pb2_grpc
import datetime
import collections
from Crypto.Cipher import AES
# from Padding import pad, unpad
# +++++++++++++++++++++++++++Padding /UNPAD +++++++++++++++++++++++++__________________________

# ==========================================================lRu cache class=====================================================
class LRUCache:
  def __init__(self,capacity):
    self.capacity=capacity
    self.list=[]
    self.cache=collections.OrderedDict(self.list)
    for k,v in self.cache.items():
      if len(v) > max_num_messages_per_user:
        v.pop()


  def get(self,key):
    try:
      value=self.cache.pop(key)
      self.cache[key]=value
      return value
    except KeyError:
      return -1

  def set(self,key,value):
    messagelist={}
    try:
      self.cache.pop(key)
    except KeyError:
      if len(self.cache) >=self.capacity:
        self.cache.popitem(last=False)
    self.list.append(value)
    self.cache[key]=self.list

  def printAll(self):
    print(self.cache)



#================================================== lru cache class ends above====================================================







_ONE_DAY_IN_SECONDS = 60 * 60 * 24

#========================================================== for individual messages======================================
senderlist = {}
receiverlist = {}

centralList={"bob":{},
             "charlie":{},
             "eve":{},
             "foo":{},
             "bar":{},
             "baz":{},
             "qux":{}

             }


ulist={"bob":{},
             "charlie":{},
             "eve":{},
             "foo":{},
             "bar":{},
             "baz":{},
             "qux":{}

             }
uulist={}


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



# ======================================================for group messages in memory==============================================
gsenderlist = {}
greceiverlist = {}

gcentralList={"bob":{},
             "charlie":{},
             "eve":{},
             "foo":{},
             "bar":{},
             "baz":{},
             "qux":{}

             }


gulist={"bob":{},
             "charlie":{},
             "eve":{},
             "foo":{},
             "bar":{},
             "baz":{},
             "qux":{}

             }
guulist={}


lruObject = LRUCache(10)

class Greeter(messenger_pb2_grpc.GreeterServicer):




    # ===========================================================for GROUP USERS =================================================
    # for group users team
    def SayHelloAgain(self,request,context):
      global lruObject
      # setting inside lru
      print(request.message1)
      userList=request.message1.split(',')
      # print("THE USER LIST ARE "+userList)
      reciev = request.message2

      lruObject.set(request.message3, reciev)
      print("printing lru")
      lruObject.printAll()
      print("printing finished lru")
      # printing lru cache

      global gsenderlist
      global greceiverlist
      global gcentralList
      global gulist
      global guulist
      # c = c + 1
      gclist = {}
      sender = userList.pop()
      print(userList)
      receiver = request.message2
      # hashKey=hashUsers(sender,receiver)

      time = datetime.datetime.now().time()
      plain_text=(request.message3)

      gclist[time] =plain_text
      guulist[time] = plain_text
      for usr in userList:
        gcentralList[usr] = gclist
      # u2[request.message2] = c
      gulist[receiver] = uulist
      print("the global list")
      # print(ulist)

      print(gcentralList)
      els = gcentralList[sender]
      return messenger_pb2.HelloReply(message=' %s!' % els)
    # for group user it ends here

    # =======================================for retrieving latest 5 messages+++++++++++++++++++++++++++++++++++++++
    def SayHello(self,request,context):

      global lruObject

      user =request.message1
      messagelist = lruObject.get(user)
      print(messagelist)
        # for k,v in messagelist:
      return messenger_pb2.HelloReply(message=' %s!' % messagelist)


    # ===================================================SIngleUSer +++++++++++++++++++++++++++++++++++++++++++++++

    # for single user
    def SayHelloAgainsecond(self, request, context):
        # f = int(request.name1) + int(request.name2)
        global lruObject
        # setting inside lru
        reciev=request.message2
        lruObject.set(reciev,request.message3)
        print("printing lru")
        lruObject.printAll()
        print("printing finished lru")
        # printing lru cache

        global senderlist
        global receiverlist
        global centralList
        global ulist
        global uulist
        # c = c + 1
        clist={}
        sender=request.message1
        receiver=request.message2
        # hashKey=hashUsers(sender,receiver)


        time=datetime.datetime.now().time()


        # Decryption
        print(request.message3)
        # plain_text= decrypt(request.message3)
        clist[time]=request.message3
        uulist[time]=request.message3
        centralList[receiver] = clist

        ulist[receiver]=uulist
        print("the global list" )
        # print(ulist)

        print(centralList)
        els =centralList[sender]
        # els=encrypt(els)
        return messenger_pb2.HelloReply(message=' %s!' % els)






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

  # docs = yaml.load_all(stream)





def serve():

    retrievevaluesfromYaml()
    global port
    portlocal='[::]:'+str(port)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    messenger_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # server.add_insecure_port('[::]:port')
    server.add_insecure_port(portlocal)
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
