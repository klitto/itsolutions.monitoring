from asyncio import sleep
from Alarm import *
from tracemalloc import start
from xmlrpc.client import boolean
import configparser
import psutil
import datetime
import getpass
import socket
import os
import time
import argparse

class Monitoring():
    '''
    Define Variables
    '''

    softlimit_ram_usage = 0
    hardlimit_ram_usage = 0

    softlimit_disk_usage = 0
    hardlimit_disk_usage = 0

    softlimit_start_time = 0
    hardlimit_start_time = 0

    softlimit_processes = 0
    hardlimit_processes = 0

    softlimit_cpu_usage = 0
    hardlimit_cpu_usage = 0

    mail_login = ""
    mail_password = ""
    mail_server = ""
    mail_to = ""

    '''
    Checks RAM Usage
    '''
    def checkRAMUsage(test = False, unittest = False):
        if unittest == True:
            ram_usage = psutil.virtual_memory()[2]
            return ram_usage

        if test == True:
            ram_usage = hardlimit_ram_usage
        else:
            ram_usage = psutil.virtual_memory()[2]

        message = ""

        if ram_usage >= hardlimit_ram_usage:
            if test == True:
                message = "TEST: Warnung: System verwendet Arbeitsspeicher in %: " + str(ram_usage)
            else:
                message = "Warnung: System verwendet Arbeitsspeicher in %: " + str(ram_usage)
        elif ram_usage >= softlimit_ram_usage:
            if test == True:
                message = "TEST: Information: System verwendet Arbeitsspeicher in %: " + str(ram_usage)
            else:
                message = "Information: System verwendet Arbeitsspeicher in %: " + str(ram_usage)
        
        Monitoring.writeLog(str(message))
        alarm = Alarm()
        alarm.sendAlarmMail(mail_login, mail_to, mail_password, mail_server, message, message)

    '''
    Checks Disk Usage
    '''

    def checkDiskUsage(test = False, unittest = False):
        if test == True:
            disk_usage = hardlimit_disk_usage
        else:
            disk_usage = psutil.disk_usage("/")[3]

        message = ""

        if unittest == True:
            return disk_usage

        if disk_usage >= hardlimit_disk_usage:
            if test == True:
                message = "TEST: Warnung: System verwendet Plattenspeicher in %: " + str(disk_usage)
            else:
                message = "Warnung: System verwendet Plattenspeicher in %: " + str(disk_usage)
        elif disk_usage >= softlimit_disk_usage:
            if test == True:
                message = "TEST: Information: System verwendet Plattenspeicher in %: " + str(disk_usage)
            else:
                message = "Information: System verwendet Plattenspeicher in %: " + str(disk_usage)

        Monitoring.writeLog(str(message))
        alarm = Alarm()
        alarm.sendAlarmMail(mail_login, mail_to, mail_password, mail_server, message, message)
    '''
    Checks Start Time
    '''

    def checkStartTime(test = False, unittest = False):
        if test == True:
            start_time = hardlimit_start_time
        else:
            start_time = round(int(time.time() - psutil.boot_time())  / 100 / 60 / 60)

        if unittest == True:
            return start_time

        message = ""

        if start_time >= hardlimit_start_time:
            if test == True:
                message = "TEST: Warnung: Systemlaufzeit in Stunden: " + str(start_time)
            else:
                message = "Warnung: Systemlaufzeit in Stunden: " + str(start_time)
        elif start_time >= softlimit_start_time:
            if test == True:
                message = "TEST: Information: Systemlaufzeit in Stunden: " + str(start_time)
            else:
                message = "Information: Systemlaufzeit in Stunden: " + str(start_time)
        
        Monitoring.writeLog(str(message))
        alarm = Alarm()
        alarm.sendAlarmMail(mail_login, mail_to, mail_password, mail_server, message, message)

    '''
    Checks Process-Count
    '''

    def checkProcesses(test = False, unittest = False):
        if test == True:
            processes = hardlimit_processes
        else:
            processes = len(psutil.pids())

        if unittest == True:
            return processes

        message = ""

        if processes >= hardlimit_processes:
            if test == True:
                message = "TEST: Warnung: Anzahl der laufenden Prozesse: " + str(processes)
            else:
                message = "Warnung: Anzahl der laufenden Prozesse: " + str(processes)
        elif processes >= softlimit_processes:
            if test == True:
                message = "TEST: Information: Anzahl der laufenden Prozesse: " + str(processes)
            else:
                message = "Information: Anzahl der laufenden Prozesse: " + str(processes)

        Monitoring.writeLog(str(message))
        alarm = Alarm()
        alarm.sendAlarmMail(mail_login, mail_to, mail_password, mail_server, message, message)

    '''
    Checks CPU Usage
    '''

    def checkCPUUsage(test = False, unittest = False):
        if test == True:
            cpu_usage = hardlimit_cpu_usage
        else:
            cpu_usage = psutil.cpu_percent(interval=None)

        if unittest == True:
            return cpu_usage

        message = ""

        if cpu_usage >= hardlimit_cpu_usage:
            if test == True:
                message = "TEST: Warnung: System verwendent CPU in %: " + str(cpu_usage)
            else:
                message = "Warnung: System verwendent CPU in %: " + str(cpu_usage)
        elif cpu_usage >= softlimit_cpu_usage:
            if test == True:
                message = "TEST: Information: System verwendent CPU in %: " + str(cpu_usage)
            else:
                message = "Information: System verwendent CPU in %: " + str(cpu_usage)

        Monitoring.writeLog(str(message))
        alarm = Alarm()
        alarm.sendAlarmMail(mail_login, mail_to, mail_password, mail_server, message, message)


    '''
    Checks User
    '''

    def checkUser():
        Monitoring.writeLog("Information: Angemeldeter Benutzer: " + str(os.getlogin()))

    '''
    Writes a Log
    '''

    def writeLog(message):
        file_path = datetime.datetime.now().strftime("%Y%m%d") + ".log"
        date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        if(os.path.exists(file_path)):
            file = open(file_path, "a")
            file.write(date + " | " + socket.gethostname() + " | " + message + "\n")
            file.close()
        else:
            file = open(file_path, "w+")
            file.write(date + " | " + socket.gethostname() + " | " + message + "\n")
            file.close()
        
        print(date + " | " + socket.gethostname() + " | " + message + "\n")

    '''
    Creates and Reads INI Config if not exists
    '''

    def readConfig():
        file_path = "config.ini"

        global softlimit_ram_usage
        global hardlimit_ram_usage

        global softlimit_disk_usage
        global hardlimit_disk_usage

        global softlimit_start_time
        global hardlimit_start_time

        global softlimit_processes
        global hardlimit_processes

        global softlimit_cpu_usage
        global hardlimit_cpu_usage

        global mail_login
        global mail_password
        global mail_server
        global mail_to


        try:
            config = configparser.ConfigParser()
            config.read(file_path)

            softlimit_ram_usage = int(config.get("tests", "softlimit_ram_usage"))
            hardlimit_ram_usage = int(config.get("tests", "hardlimit_ram_usage"))

            softlimit_disk_usage = int(config.get("tests", "softlimit_disk_usage"))
            hardlimit_disk_usage = int(config.get("tests", "hardlimit_disk_usage"))

            softlimit_start_time = int(config.get("tests", "softlimit_start_time"))
            hardlimit_start_time = int(config.get("tests", "hardlimit_start_time"))

            softlimit_processes = int(config.get("tests", "softlimit_processes"))
            hardlimit_processes = int(config.get("tests", "hardlimit_processes"))

            softlimit_cpu_usage = int(config.get("tests", "softlimit_cpu_usage"))
            hardlimit_cpu_usage = int(config.get("tests", "hardlimit_cpu_usage"))

            mail_login = config.get("mail", "mail_login")
            mail_password = config.get("mail", "mail_password")
            mail_server = config.get("mail", "mail_server")
            mail_to = config.get("mail", "mail_to")
        except Exception:
            print("Es ist ein Fehler beim Aufruf der Konfiguration aufgetreten!")

            file = open(file_path, "w")
            file.write("[tests]\n\nsoftlimit_ram_usage = 75\nhardlimit_ram_usage = 90\nsoftlimit_disk_usage = 75\nhardlimit_disk_usage = 90\nsoftlimit_start_time = 24\nhardlimit_start_time = 48\nsoftlimit_processes = 200\nhardlimit_processes = 250\nsoftlimit_cpu_usage = 75\nhardlimit_cpu_usage = 90\n\n[mail]\nmail_login = user\nmail_password = password\nmail_server = server\nmail_to = reciever")
            file.close()

            config = configparser.ConfigParser()
            config.read(file_path)

            softlimit_ram_usage = int(config.get("tests", "softlimit_ram_usage"))
            hardlimit_ram_usage = int(config.get("tests", "hardlimit_ram_usage"))

            softlimit_disk_usage = int(config.get("tests", "softlimit_disk_usage"))
            hardlimit_disk_usage = int(config.get("tests", "hardlimit_disk_usage"))

            softlimit_start_time = int(config.get("tests", "softlimit_start_time"))
            hardlimit_start_time = int(config.get("tests", "hardlimit_start_time"))

            softlimit_processes = int(config.get("tests", "softlimit_processes"))
            hardlimit_processes = int(config.get("tests", "hardlimit_processes"))

            softlimit_cpu_usage = int(config.get("tests", "softlimit_cpu_usage"))
            hardlimit_cpu_usage = int(config.get("tests", "hardlimit_cpu_usage"))

            mail_login = config.get("mail", "mail_login")
            mail_password = config.get("mail", "mail_password")
            mail_server = config.get("mail", "mail_server")
            mail_to = config.get("mail", "mail_to")

    def readArguments():
        parser = argparse.ArgumentParser(description="Client Monitoring")
        parser.add_argument('-t', '--test', type=bool, metavar='', required=False, help='Führe einen Test mit fiktiven Werten durch')
        parser.add_argument('-sram', '--softlimit_ram_usage', type=int, required=False, help='Ändere das Softlimit für die RAM Auslastung')
        parser.add_argument('-hram', '--hardlimit_ram_usage', type=int, required=False, help='Ändere das Hardlimit für die RAM Auslastung')
        parser.add_argument('-uram', '--use_ram_usage', type=bool, required=False, help='Überwache die RAM Auslastung')
        parser.add_argument('-sdu', '--hardlimit_disk_usage', type=int, required=False, help='Ändere das Softlimit für die Disk Auslastung')
        parser.add_argument('-hdu', '--softlimit_disk_usage', type=int, required=False, help='Ändere das Hardlimit für die Disk Auslastung')
        parser.add_argument('-udu', '--use_disk_usage', type=bool, required=False, help='Überwache die Disk Auslastung')
        parser.add_argument('-sst', '--softlimit_start_time', type=int, required=False, help='Ändere das Softlimit für die Start Time')
        parser.add_argument('-hst', '--hardlimit_start_time', type=int, required=False, help='Ändere das Hardlimit für die Start Time')
        parser.add_argument('-ust', '--use_start_time', type=bool, required=False, help='Überwache die Start Time')
        parser.add_argument('-sp', '--softlimit_processes', type=int, required=False, help='Ändere das Softlimit für die Anzahl der Prozesse')
        parser.add_argument('-hp', '--hardlimit_processes', type=int, required=False, help='Ändere das Hardlimit für die Anzahl der Prozesse')
        parser.add_argument('-up', '--use_processes', type=bool, required=False, help='Überwache die Anzahl der Prozesse')
        parser.add_argument('-scu', '--softlimit_cpu_usage', type=int, required=False, help='Ändere das Softlimit für die CPU Auslastung')
        parser.add_argument('-hcu', '--hardlimit_cpu_usage', type=int, required=False, help='Ändere das Hardlimit für die CPU Auslastung')
        parser.add_argument('-ucu', '--use_cpu_usage', type=bool, required=False, help='Überwache die CPU Auslastung')
        parser.add_argument('-ml', '--mail_login', type=str, required=False, help='Ändere den Mail Benutzernamen')
        parser.add_argument('-mp', '--mail_password', type=str, required=False, help='Ändere das Mail Passwort')
        parser.add_argument('-ms', '--mail_server', type=str, required=False, help='Ändere den Mailserver')
        parser.add_argument('-mt', '--mail_to', type=str, required=False, help='Ändere den Mailempfänger')
        args = parser.parse_args()

        return args

if __name__ == "__main__":
    Monitoring.readConfig()

    change_settings = 0

    args = Monitoring.readArguments()
    
    if args.test == True:
        Monitoring.checkCPUUsage(test=True)
        Monitoring.checkDiskUsage(test=True)
        Monitoring.checkProcesses(test=True)
        Monitoring.checkRAMUsage(test=True)
        Monitoring.checkStartTime(test=True)
        Monitoring.checkUser()

    '''
    Edit Config if Args are given
    '''

    if args.softlimit_ram_usage != None:
        change_settings += 1
        
        file_path = "config.ini"
        
        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(args.softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""
        
        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.hardlimit_ram_usage != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(args.hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""
        
        file = open(file_path, "w+")
        file.write(config_input)
        file.close()
        
        Monitoring.readConfig()
    if args.softlimit_disk_usage != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(args.softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""
        
        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.hardlimit_disk_usage != None:
        change_settings += 1

        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(args.hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""
        
        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.softlimit_start_time != None:
        change_settings += 1

        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(args.softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""
        
        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.hardlimit_start_time != None:
        change_settings += 1
        
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(args.hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.softlimit_processes != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(args.softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.hardlimit_processes != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(args.hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.softlimit_cpu_usage != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(args.softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.hardlimit_cpu_usage != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(args.hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.mail_login != None:
        change_settings += 1

        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(args.mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.mail_password != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(args.mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.mail_server != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(args.mail_server) + "\nmail_to = " + str(mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()
    if args.mail_to != None:
        change_settings += 1
            
        file_path = "config.ini"

        config_input = "[tests]\n\nsoftlimit_ram_usage = " + str(softlimit_ram_usage) + "\nhardlimit_ram_usage = " + str(hardlimit_ram_usage) + "\nsoftlimit_disk_usage = " + str(softlimit_disk_usage) + "\nhardlimit_disk_usage = " + str(hardlimit_disk_usage) + "\nsoftlimit_start_time = " + str(softlimit_start_time) + "\nhardlimit_start_time = " + str(hardlimit_start_time) + "\nsoftlimit_processes = " + str(softlimit_processes) + "\nhardlimit_processes = " + str(hardlimit_processes) + "\nsoftlimit_cpu_usage = " + str(softlimit_cpu_usage) + "\nhardlimit_cpu_usage = " + str(hardlimit_cpu_usage) + "\n\n[mail]\nmail_login = " + str(mail_login) + "\nmail_password = " + str(mail_password) + "\nmail_server = " + str(mail_server) + "\nmail_to = " + str(args.mail_to) + ""

        file = open(file_path, "w+")
        file.write(config_input)
        file.close()

        Monitoring.readConfig()

    '''
    Starts the infinite loop
    '''

    if change_settings == 0 and args.test == None:
        while True:
            if args.use_ram_usage == True:
                Monitoring.checkRAMUsage()
            if args.use_disk_usage == True:
                Monitoring.checkDiskUsage()
            if args.use_start_time == True:
                Monitoring.checkStartTime()
            if args.use_processes == True:
                Monitoring.checkProcesses()
            if args.use_cpu_usage == True:
                Monitoring.checkCPUUsage()
            Monitoring.checkUser()
            time.sleep(600)