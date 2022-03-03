from django.contrib.auth.hashers import make_password

import sys
import os
import csv
sys.path.append('/userproject/userproject/userproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

f = open("Today001.csv", "r")
reader = csv.reader(f)
data = [ e for e in reader ]
print(data)
f.close()

for i in range(len(data)-1):
    password = data[i+1][1]
    yy = make_password(password, salt=None, hasher='default')
    data[i+1][1]=yy

f = open('yesterday.csv', 'w', newline='')
writer = csv.writer(f)
writer.writerows(data)
f.close()

