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
from . import views

from subprocess import run,PIPE
data= ""
hostname= ""
def button(request):
    return render(request,'home.html')

def output(request):
   data=request.session['data'] +"\n"+ request.session['IP']
   data= data +"\n"+ request.session['username'] 
   image=request.POST.get('dldImage')
   data= data+"\n"+ image
   return render(request,'home.html',{'data':data}) 

def external(request):

   hostname= request.POST.get('param1')
   username = request.POST.get('param2')
   password = request.POST.get('param3')
   request.session['IP'] = hostname
   request.session['username'] = username
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
   remote_conn_pre.connect(hostname, port=22, username=username, password=password, look_for_keys=False, allow_agent=False)
   data= data+"\n" + "SSH connection established to " + hostname
   remote_conn = remote_conn_pre.invoke_shell()
#   return render(request,'home.html',{'data':data})
#
# extract show version output
# Disable pagination in the termial
#
    
   remote_conn.send("terminal length 0 \n")
   remote_conn.send("\n")
   remote_conn.send("show version\n")
   remote_conn.send("\n")
   time.sleep(5)
   if remote_conn.recv_ready():
         
            show_version = remote_conn.recv(500)
            data= data + "\n" + show_version.decode()
            message= "Kindly proceed with upgrade by selecting new image"
            data= data + "\n\n\n"+"############################################################"+"\n"+"############################################################"+"\n\n"+message +"\n\n" +"############################################################"+"\n"+"############################################################"

            
   remote_conn.send("\n")
#
#
   
   return render(request,'home.html',{'data':data})

