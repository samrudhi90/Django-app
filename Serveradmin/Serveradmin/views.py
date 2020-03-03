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
   
   return render(request,'home.html',{'data1':data1}) 
