command_python = "python server.py"
command_npm = "cd Bengali-Spell-Checker-Word-Add-in && npm start"

python = ''
npm = ''

import threading
import os
import subprocess
from subprocess import Popen, PIPE
import sys
from win10toast import ToastNotifier
toaster = ToastNotifier()
icon_path = 'icon.ico'
notification_title = 'Bengali Spell Checker'

def show_notification(message = ''):
    while toaster.notification_active(): 
        time.sleep(0.5)
    toaster.show_toast(notification_title, message, threaded=True, duration=5, icon_path = icon_path)

show_notification('Starting...')
from infi.systray import SysTrayIcon
def on_quit_callback(systray):
    kill_process_on_port(8088)
    kill_process_on_port(5000)
    print('Quiting Now...')
    show_notification('Server has been shut down')
    systray.shutdown()
    
systray = SysTrayIcon(icon_path, "Bengali Spell Checker", on_quit = on_quit_callback)
systray.start()

def run_python_thread():
    python_process = subprocess.Popen([command_python], stdout=PIPE, stderr=PIPE, shell=True)
    fg = 0
    cnt = 0
    for line in iter(python_process.stdout.readline, ''):  # replace '' with b'' for Python 
        if len(line) < 6:
            cnt += 1
        else: cnt = 0
        print(cnt)
        if cnt > 3:
            break
        if fg == 0:
            fg = 1
            show_notification('Server has started. ')
        sys.stdout.write(line)
def run_python():
    global python
    python = threading.Thread(target=run_python_thread)
    python.start()
    print('Running Python command')

def kill_process_on_port(port):
    process = Popen(["netstat", "-ano", "|", "findstr", ":{0}".format(port)], stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    print(stdout)
    for line in str(stdout.decode("utf-8")).split("\n"): 
        print(line)
        data = [x for x in line.split() if x != '']
        print(data)
        if (len(data) <= 1):
            continue
        pid = data[-1].strip()
        print('Found ', pid)
        if pid == 0:
            continue
        os.system('taskkill /pid {0} /f'.format(pid))

kill_process_on_port(8088)
kill_process_on_port(5000)

run_python()
import time

import sys

try:
    import uwsgi
    ex = os.path.join(uwsgi.opt['home'], 'bin/python') # or some default location
except (ImportError, KeyError):
    ex = sys.executable
    print(ImportError)
    print(KeyError)

print(sys.executable)
kill_process_on_port(5000)
import os
os.system("python server.py")
proc = subprocess.call(['E:\\Program Files\\Python37\\pythonw.exe', 'server.py'], shell=True, stdout=subprocess.PIPE)
print(proc)
#menu_options = (("Say Hello", None, say_hello), )

#subprocess.run(["pip", "install", "nltk"], shell=True, check=True)
#command = 'pip download -r requirements.txt -d libraries'
#subprocess.run(command.split(), shell=True, check=True)

