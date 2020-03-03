import os

response = os.system("ping -c 1 " + param)
if response == 0:
   data1=param + ", is up!"
else:
 data1=param + ", is down!"