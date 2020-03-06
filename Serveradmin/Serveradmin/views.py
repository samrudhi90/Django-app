from django.shortcuts import render
import os
import sys
import getpass
import sys
import telnetlib
import time
import paramiko
import html
from django.utils.html import format_html
from io import StringIO
import io
import datetime
from . import views

from subprocess import run,PIPE
data= ""
hostname= ""
def button(request):
    return render(request,'home.html')

def output(request):
   hostname=request.session['IP']
   username=request.session['username']
   password=request.session['password']
   image=request.POST.get('dldImage')
   current_time=datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
   fd = open('Device_Upgrade'+current_time+ '.txt', 'w')
   old_stdout = sys.stdout
   sys.stdout = fd
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   remote_conn_pre.connect(hostname, port=22, username=username, password=password, look_for_keys=False, allow_agent=False)
   remote_conn = remote_conn_pre.invoke_shell()
   print("……………….CISCO COMMAND SHOW BOOTVAR OUTPUT………………….\n")
   remote_conn.send("show bootvar \n")
   time.sleep(1)
   output=remote_conn.recv(65535)
   print(output)
   remote_conn.send("sh run | redirect bootflash:logsBITS.txt \n")
   time.sleep(5)
   remote_conn.send("show version \n")
   time.sleep(1)
   output=remote_conn.recv(1000)
   print(output)
   remote_conn.send("conf t \n")
   remote_conn.send("no boot system \n")
   remote_conn.send("boot system flash bootflash:" + image)
   data = "Image Name:" + image
   remote_conn.send("\n")
   remote_conn.send("exit \n")
   time.sleep(2)
   remote_conn.send("wr \n")
   time.sleep(2)
   remote_conn.send("reload \n")
   time.sleep(5)
   remote_conn.send("\n")
   
   message= """Switch has been configured and reloading now"""
   output=remote_conn.recv(65535)
   fd.close()
   data=request.session['data'] +"\n" + output.decode()
   
   return render(request,'home.html',{'data':data})


def external(request):


   
   hostname= request.POST.get('param1')
   username = request.POST.get('param2')
   password = request.POST.get('param3')
   request.session['IP'] = hostname
   request.session['username'] = username
   request.session['password'] = password
   response = os.system("ping -c 1 " + hostname)

   if response == 0:
       data=hostname + ", is up!"
       
   else:
       data=hostname + ", is down!"
       request.session['data'] = data
       return render(request,'home.html',{'data':data.strip()}) 

#
# save host login info
#

#
# We first set up ssh session.
#
   
   remote_conn_pre = paramiko.SSHClient()
   remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   try:
      remote_conn_pre.connect(hostname, port=22, username=username, password=password, look_for_keys=False, allow_agent=False)
      data= data+"\n" + "SSH connection established to " + hostname
   except paramiko.AuthenticationException:
      data=data+"\n"+"Authentication failed "
      return render(request,'home.html',{'data':data})
   remote_conn = remote_conn_pre.invoke_shell()

# extract show version output
# Disable pagination in the termial
#
   
   remote_conn.send("terminal length 0 \n")
   remote_conn.send("\n")
   remote_conn.send("show version\n")
   remote_conn.send("\n")
   time.sleep(5)
   if remote_conn.recv_ready():
         
            show_version = remote_conn.recv(65535)
            data= data + "\n" + show_version.decode()
            message= "Kindly proceed with upgrade by selecting new image"
            data= data + "\n\n\n"+"############################################################"+"\n"+"############################################################"+"\n\n"+message +"\n\n" +"############################################################"+"\n"+"############################################################"

            
   remote_conn.send("\n")
   request.session['data']=data
#
#
   
   return render(request,'home.html',{'data':data})

