import sys,os
from urllib import urlopen
from urllib import urlretrieve
from urllib2 import URLError,HTTPError
import commands
import subprocess
import argparse
import random
from PIL import Image
import os
import os.path

def cmd(cmd):
  return commands.getoutput(cmd)

# arguments
parser = argparse.ArgumentParser()
parser.add_argument('--data_dir',        type=str,   default='images')
parser.add_argument('--num_of_pics',   type=int,   default=1500)
parser.add_argument('--wnid',  type=str)

args = parser.parse_args()

dict={}
for line in open('words.txt', 'r'):
  line=line.split()
  dict[line[0]]=line[1]

ids = open('imagenet.synset.obtain_synset_list', 'r').read()
ids = ids.split()
random.shuffle(ids)

if(os.path.exists('./images/') == False):
  os.mkdir('./images/')

id = args.wnid

category = dict[id]
cnt = 0
if len(category)>0:
  cmd("mkdir %s/%s"%(args.data_dir,category))
  print(category)
  try:
    urls=urlopen("http://www.image-net.org/api/text/imagenet.synset.geturls?wnid="+id).read()
    urls=urls.split()
    random.shuffle(urls)

    j=0
    while cnt<args.num_of_pics if args.num_of_pics<len(urls) else len(urls):
      url = urls[j]
      j+=1
      if j>=len(urls):
        break
      print(url)
      filename = os.path.split(url)[1]
      try:
        output = "%s/%s/%d_%s"%(args.data_dir,category,cnt,filename)
        urlretrieve(url,output )
        try:
          img = Image.open(output)
          size = os.path.getsize(output)
          if size==2051: #flickr Error
            cmd("rm %s"%output)
            cnt-=1
        except IOError:
          cmd("rm %s"%output)
          cnt-=1
      except HTTPError, e:
        cnt-=1
        print e.reason
      except URLError, e:
        cnt-=1
        print e.reason
      except IOError, e:
        cnt-=1
        print e
      cnt+=1
  except HTTPError, e:
    print e.reason
  except URLError, e:
    print e.reason
  except IOError, e:
    print e
