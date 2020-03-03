from django.shortcuts import render
import os
import sys
import getpass
import sys
import telnetlib
import time

from subprocess import run,PIPE

def button(request):
    return render(request,'home.html')



def external(request):

   HOST= request.POST.get('param1')
   user = request.POST.get('param2')
   

   response = os.system("ping -c 1 " + HOST)

   if response == 0:
       data1=HOST + ", is up!"
   else:
       data1=HOST + ", is down!"
  
  
   password = getpass.getpass()
   Image_name = "cat4500-entservicesk9-mz.150-2.SG7.bin"
   tn = telnetlib.Telnet(HOST)

   tn.read_until("Username: ")
   tn.write(user + "\n")

   if password:
      tn.read_until("Password: ")
      tn.write(password + "\n")

  print ("Capturing and printing pre-upgrade logs. Please wait......")
# Below commands are to capture pre outputs!! 
  tn.write("enable \n")
  tn.write("ter len 0 \n")
  tn.write("show version \n")
  tn.write("show bootvar \n")
  tn.write("show run \n")
  time.sleep(15)
           
  tn.write("\n")

# Below is to configure parameters and to exit:

  print ("Starting to upgrade now")

# Below syntax is to start upgrade

  tn.write("conf t\n")
  tn.write("no boot system \n")
  tn.write("boot system flash bootflash:")
  tn.write(Image_name)
  tn.write("\n")
  tn.write("exit \n")
  tn.write("write memory \n")
  tn.write("show bootvar \n")
  tn.write("reload \n")
  time.sleep(1)

  tn.read_until("Proceed with reload?")

  tn.write("yes \n")

  print tn.read_all()
   
  return render(request,'home.html',{'data1':data1}) 
