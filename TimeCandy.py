#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' 
MIT License
Copyright (c) <2017> <Watanuki Soren>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

#TimeCandy for Melbourne University
#by Watanuki Soren
#Automatically retrive/parse timetable info from prod.unimelb.edu.au
import requests
import getpass
import sys
import os
import re
#import matplotlib.pyplot as plt
from lxml import html
from bs4 import BeautifulSoup
from multiprocessing import Queue
import socket

def connect(server):
  try:
    host = socket.gethostbyname(server)
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

#FETCH SYSTEM PLATFORM INFO
if "idlelib" in sys.modules:
    def cls(): 
        print("\n" * 100)
else:
    if sys.platform in ['win32' , 'cygwin']:
        def cls():
            os.system('cls')
    else:
        def cls():
            os.system('clear')        

#MAIN FUNCTION            
def time_candy():
    #CLEAN SCREEN
    cls()
    #VALIDATE CONNECTION
    print('----------------------------------')
    print('TimeCandy 1.10 | by Watanuki Soren')
    print('----------------------------------') 
    print('Connecting to Melbourne University Timetabling Server...')
    if not connect('prod.ss.unimelb.edu.au'):
        if connect('stackoverflow.com'):
            cls()
            print('Error: Server Down.')
            print('Melbourne University\' server might be down.')
            print('Please report this issule to your IT department.')
            print('press any key...')
            input()
            return 'Error_3'
        else:
            cls()
            print('Error: No internet.')
            print('Unable to establish connection with the remote server.')
            print('Please check your internet connection.')
            print('press any key...')
            input()
            return 'Error_4'
            
    #README
    cls()    
    print('----------------------------------')
    print('TimeCandy 1.10 | by Watanuki Soren')
    print('----------------------------------')
    print('-----------------')
    print('UoM Student Login')
    print('-----------------')
    
    #GET LOGIN CREDENTIAL
    u_lock, p_lock = 1, 1

    while u_lock:
        username = input('Username: ')
        if username == '':
            print('Error: Username cannot be empty.')
        else:
            u_lock = 0
 
    while p_lock:
        password = getpass.getpass('Password: ')
        if password == '':
            print('Error: Password cannot be empty.')
        else:
            p_lock = 0       
    cls()
    print('----------------------------------')
    print('TimeCandy 1.10 | by Watanuki Soren')
    print('----------------------------------') 
    print('Logining in...')
    
    #FETCH SESSION DATA
    r = requests.session()
    login_url = 'https://prod.ss.unimelb.edu.au/student/login.aspx'
    result = r.get(login_url)
    tree = html.fromstring(result.text)
    __EVENTVALIDATION = list(set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))
    __VIEWSTATEGENERATOR = list(set(tree.xpath("//input[@name='__VIEWSTATEGENERATOR']/@value")))
    __VIEWSTATE = list(set(tree.xpath("//input[@name='__VIEWSTATE']/@value")))
    __EVENTARGUMENT = list(set(tree.xpath("//input[@name='__EVENTARGUMENT']/@value")))
    __EVENTTARGET = list(set(tree.xpath("//input[@name='__EVENTTARGET']/@value")))

    #PREAPARE PAYLOAD
    payload={'ctl00$Content$txtUserName$txtText' : username,
                    'ctl00$Content$txtPassword$txtText' : password,
                    '__EVENTVALIDATION': __EVENTVALIDATION,
                    '__VIEWSTATEGENERATOR' : __VIEWSTATEGENERATOR,
                    '__VIEWSTATE' : __VIEWSTATE,
                    '__EVENTARGUMENT' : __EVENTARGUMENT,
                    '__EVENTTARGET' : 'ctl00$Content$cmdLogin'}

    #COMMIT LOGIN
    result = r.post(login_url, data = payload)

    #HTML VISIBLE VALIDATOR
    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        elif element in ['\n', '\t', ' ', '']:
            return False
        return True
        
    #VALIDATE SESSION
    if not 'eStudent' in result.text:
        cls()
        print('----------------------------------')
        print('TimeCandy 1.10 | by Watanuki Soren')
        print('----------------------------------')        
        print('Login Attempt Failed: Invalid Credential.')
        print('your username and password might be wrong.')
        print('press any key...')
        input()
        time_candy()
        return('ERROR2')
    else:
        url = 'https://prod.ss.unimelb.edu.au/student/SM/PersDtls10.aspx?r=%23UM.STUDENT.APPLICANT&f=$S1.EST.PERSDTLS.WEB'
        result = r.get(url)
        tree = html.fromstring(result.text)
        first_name = list(set(tree.xpath("//input[@name=\"ctl00$Content$txtGivenName$InputControl\"]/@value")))[0]
        cls()
        print('----------------------------------')
        print('TimeCandy 1.10 | by Watanuki Soren')
        print('----------------------------------') 
        print('Welcome, ' + first_name +'!')
        print('Fetching Data...')
        
    #FETCH DATA
    url = 'https://prod.ss.unimelb.edu.au/student/SM/StudentTtable10.aspx?r=%23UM.STUDENT.APPLICANT&f=%24S1.EST.TIMETBL.WEB'
    result = r.get(url)
    
    #VALIDATE DATA
    if 'CREM' not in result.text:
        print('----------------------------------')
        print('TimeCandy 1.10 | by Watanuki Soren')
        print('----------------------------------')        
        print('Timetable Error: ')
        print('This program cannot analyse your timetable.')
        print('Please contact me at aaronduooo@gmail.com.')
        print('with your info attached: current major,  current semester and degree history.')
        print('this error is expected and very important, thanks.')
        return 'Error_2'
    
    #EXTRACT TIMETABLE INFO
    tree = html.fromstring(result.text)
    list(set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))
    
    #PARSE DATA
    cls()
    print('----------------------------------')
    print('TimeCandy 1.10 | by Watanuki Soren')
    print('----------------------------------')        
    print('Parsing html document...')
    soup = BeautifulSoup(result.text, "lxml")
    data = soup.findAll(text=True)
 
    result = list(filter(visible, data))
    new_list = []
    for item in result:
        new_item = re.sub('\s+', '', item)
        new_list.append(new_item)
        
    start_index = new_list.index('Monday')
    end_index = new_list.index('Help')
    new_list = new_list[start_index: end_index]
    
    #ANALYSE
    cls()
    print('----------------------------------')
    print('TimeCandy 1.10 | by Watanuki Soren')
    print('----------------------------------') 
    print('Analysing timetable data...')
    url = 'https://prod.ss.unimelb.edu.au/student/SM/PersDtls10.aspx?r=%23UM.STUDENT.APPLICANT&f=$S1.EST.PERSDTLS.WEB'
    result = r.get(url)
    tree = html.fromstring(result.text)
    full_name = list(set(tree.xpath("//input[@name=\"ctl00$Content$txtFormalName1$InputControl\"]/@value")))[0]
    
    mon_index = 0
    tue_index = new_list.index('Tuesday')
    wed_index = new_list.index('Wednesday')
    thu_index = new_list.index('Thursday')
    fri_index = new_list.index('Friday')
    
    mon_data = new_list[1: tue_index]
    tue_data = new_list[tue_index+1: wed_index]
    wed_data = new_list[wed_index+1: thu_index]
    thu_data = new_list[thu_index+1: fri_index]
    fri_data = new_list[fri_index+1: ]
    
    cls()
    print('----------------------------------')
    print('TimeCandy 1.10 | by Watanuki Soren')
    print('----------------------------------') 
    print('Student: ' + full_name)
    print('--------------------------------------')
    data_collection = [mon_data, tue_data, wed_data, thu_data, fri_data]
    day_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    day_count=0
    database=[]
   
    for data in data_collection:
        class_count = int(len(data)/4)
        print(day_list[day_count])
        count=class_count-1
        while count+1:
            classes = data[4*count: 4*count+4]
            class_type=''.join([i for i in classes[0] if i.isalpha()])
            class_room=classes[2]
            if 'Parkville' in classes[2]:
                class_room = classes[2][9:]
           
            print(classes[1][1:], classes[3], class_type, class_room)
            
            '''class_time= classes[3]
            class_time_start = classes[3]
            class_time_end = 
            
            database.append([day_count, classes[1][1:], classes[3], class_type, class_room])
            '''
            count-=1
        
        day_count+=1
        print('\n')
    
    print('↑↑ Scroll up for full timetable ↑↑')
    
    
    #fig=plt.figure(figsize=(10,5.89))
    
    
    
    
if __name__ == '__main__':
    time_candy()


