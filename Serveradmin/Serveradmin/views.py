from django.shortcuts import render
import os
import sys
import getpass
import sys
import telnetlib
import time
import paramiko


from subprocess import run,PIPE
data= ""
hostname= ""
def button(request):
    return render(request,'home.html')

def output(request):

   hostname= request.POST.get('param1')
   
   response = os.system("ping -c 1 " + hostname)

   if response == 0:
       data=hostname + ", is up!"
       
   else:
       data=hostname + ", is down!"
   return render(request,'home.html',{'data':data}) 

def external(request):

   hostname= request.POST.get('param1')
   username = request.POST.get('param2')
   password = request.POST.get('param3')

 

#
# save host login info
#

#
# We first set up ssh session.
#

remote_conn_pre = paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(hostname, port=22, username=username, password=password, look_for_keys=False, allow_agent=False)
print("SSH connection established to " + hostname)
remote_conn = remote_conn_pre.invoke_shell()

#
# extract show version output
# Disable pagination in the termial
#
remote_conn.send("terminal length 0\n")
remote_conn.send("\n")
remote_conn.send("show version\n")
remote_conn.send("\n")
time.sleep(5)
if remote_conn.recv_ready():
        show_version = remote_conn.recv(1000)
#
# To print the CLI "output" as seen in the CLI it needs to
# be formatted in String format "str" "utf-8" as shown below
#
show_version_str = show_version.decode('utf-8')
platform_version_lst = platform_version_lst
#
# Extract version information
#

for platform_version in show_version_str.splitlines():
    if 'Cisco IOS Software' in platform_version:
        print (platform_version)
platform_version_lst = platform_version
platform_version_lst = platform_version_lst.split()
print ( platform_version_lst )	
#
remote_conn.send("\n")
#
#
   
   return render(request,'home.html',{'data1':data1}) 
