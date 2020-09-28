import pyttsx3
import datetime 
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os
import pyautogui
import random
import fnmatch
import json
import requests
import time
import face_recognition
from PIL import Image
from urllib.request import urlopen
# ! ------ INI Instalaciones ------
# ? pip install pyautogui
# ? pip install pyttsx3
# ? pip install speechRecognition
# ? pip install speechRecognition
# ? pip install wikipedia
# ? pip install psutil
# ? pip install pyjokes
# ? pip install face_recognition
# ! ------ FIN Instalaciones ------

engine = pyttsx3.init()
engine.setProperty('rate',130) # velocidad del habla
engine.setProperty('voice','spanish') # poner el idioma en el que tiene que hablar
engine.setProperty('volume',1) # volumen 0.1 (min) a 1 (max)

def Speak(audio):
    engine.say(audio)
    engine.runAndWait()

def Jokes():
    Speak(pyjokes.get_joke('es'))

def Screenshot():
    img = pyautogui.screenshot()
    img.save('C:/Vibra/Trash/screenshot/trash.png')

def TimeNow():
    time=datetime.datetime.now().strftime('%H:%M:%S') #Formato 24Horas
    Speak('La hora actual es')
    Speak(time)

def DateNow():
    date=datetime.datetime.now().strftime('%d/%m/%Y')
    Speak('El día de hoy es')
    Speak(date)

def Exit():
    Speak('Gracias. Espero haberte sido de utilidad')
    quit()

def Wishes():
    DateNow()
    TimeNow()
    hour = datetime.datetime.now().hour
    if hour>6 and hour<12: Speak('Buenos dias!')
    elif hour>=12 and hour<20: Speak('Buenas tardes!')
    elif hour>=20 and hour<24: Speak('Buenas noches!')
    else: Speak('Estas en la madrugada, deberías de estar durmiendo!')

def TakeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print ('Escuchando...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio=r.listen(source)
    try:
        print('Reconociendo Voz ...')
        query= r.recognize_google(audio,language='es-ES')
        print(query)
    except Exception as e:
        print(e)
        print('¿Puedes Repetirlo?')
        return 'None'
    return query

def SendEmail(to,content):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    #? Para que se puedan enviar correos hay que habilitar la seguridad baja en gmail.
    server.login('correoenviador','contraseña')
    server.sendmail('correoenviador',to,content)
    server.close()

def CpuUtils():
    usage= str(psutil.cpu_percent())
    Speak('Uso de CPU' + usage)

def Faces():
    img= face_recognition.load_image_file('C:\Vibra\Trash\photos\persons.jpg')
    loc= face_recognition.face_locations(img)
    for face_location in loc:
        top,right,bottom,left = face_location
        face_img=img[top:bottom,left:right]
        pil_img= Image.fromarray(face_img)
        pil_img.save(f'C:\Vibra\Trash\photos\{top}.jpg')

if __name__ == '__main__':
    while True:
        query= TakeCommand().lower()
        if 'hora' in query: #dime la hora cuando lo pregunte
            TimeNow()
        elif 'día' in query: #dime el dia cuando lo pregunte
            DateNow()
        elif 'wikipedia' in query: #busca en wikipedia
            Speak('Buscando...')
            query=query.replace('wikipedia','')
            wikipedia.set_lang('es')
            result=wikipedia.summary(query,sentences=3)
            Speak('Segun wikipedia')
            print(result)
            Speak(result)
        elif 'enviar correo' in query:
            try:
                Speak('¿Que quieres que escriba en el correo?')
                content=TakeCommand()
                #decir a quien va el correo
                Speak('Quien es el receptor?')
                receiver=input('Escribe el receptor del email:')
                to= receiver
                SendEmail(to,content)
                Speak(content)
                Speak('Email enviado correctamente')
            except Exception as e:
                print(e)
                Speak('Hay Problemas para enviar correo')
        elif 'buscar dominio' in query:
            Speak('¿Que quieres buscar?')
            chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            search = TakeCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com') #solo abre websites con ".com" al final
        elif 'youtube' in query:
            Speak('¿Que quieres buscar?')
            chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            search_term= TakeCommand().lower()
            Speak('Vamos a buscarlo en youtube')
            wb.get(chromepath).open('https://www.youtube.com/results?search_query='+ search_term)
        elif 'google' in query:
            Speak('¿Que quieres buscar?')
            search_term= TakeCommand().lower()
            Speak('Buscando...')
            chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            wb.get(chromepath).open('https://www.google.com/search?q='+ search_term)
        elif 'datos' in query:
            Wishes()
        elif 'ordenador' in query:
            CpuUtils()
        elif 'chiste' in query:
            Jokes()
        elif 'salir' in query:
            Exit()
        elif 'caras' in query:
            Faces()
        elif 'producción de música' in query:
            Speak('Abriendo el programa Ableton')
            ableton = r'C:/Ableton/Live 10 Suite/Program/Ableton Live 10 Suite.exe'
            os.startfile(ableton)
        elif 'quiero notas' in query:
            Speak('¿Que quieres que escriba?')
            notes= TakeCommand()
            file = open('notas.txt','w')
            Speak('Quieres que añada el dia y la hora?')
            ans = TakeCommand()
            if 'sí' in ans or 'si' in ans:
                strtime=datetime.datetime.now().strftime('%H:%M:%S')
                file.write(strtime)
                file.write(":-")
                file.write(notes)
                Speak ('Todo Listo') 
            else:
                file.write(notes)
        elif 'ver notas' in query:
            Speak('Viendo Notas Grabadas')
            file = open('notas.txt','r')
            print(file.read())
            Speak(file.read())
        elif 'captura de pantalla' in query:
            Screenshot()
            Speak('Captura de pantalla realizada')
        elif 'poner música' in query:
            songs_dir = 'C:/Vibra/Trash/music'
            music =fnmatch.filter(os.listdir(songs_dir), '*.mp3')
            Speak('¿Que canción tengo que poner?')
            Speak('Selecciona un número de un total de ' +str(len(music)) + ' canciones o di las palabras ELIGE TU')
            ans = TakeCommand().lower()
            while('número' not in ans and 'elige tú' not in ans):
                Speak('no te he entendido, repite')
                ans = TakeCommand().lower()
            if 'número' in ans:
                no= int(ans.replace('número',''))
            elif 'elige tú' in ans:
                no=random.randint(0,len(music)-1)
            os.startfile(os.path.join(songs_dir,music[no]))
        elif 'recuerda esto' in query:
            Speak('que quieres que recuerde?')
            memory=TakeCommand()
            Speak('dijiste que recordara lo siguiente: ' + memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()
        elif 'te acuerdas' in query:
            remember = open('memory.txt','r')
            Speak('me dijiste que recordara lo siguiente:'+ remember.read())
        elif 'dónde está' in query:
            query = query.replace('dónde está','')
            location = query
            speakOffline('Pediste la localizacion de ' + location)
            chromepath = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            wb.get(chromepath).open('https://www.google.com/maps/place/'+location)
        elif 'deja de escuchar' in query:
            speakOffline('cuantos segundos tengo que dejar de escuchar?')
            ans= int(TakeCommand())
            speakOffline('dejo de escuchar durante ')
            time.sleep(ans)
        elif 'cerrar sesión' in query:
            os.system('shutdown -l')
        elif 'reiniciar' in query:
            os.system('shutdown /r /t 1')
        elif 'apagar' in query:
            os.system('shutdown /s /t 1')