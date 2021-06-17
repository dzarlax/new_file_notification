import schedule
from os import listdir
from os.path import isfile, join
import requests
import os
import time

def convert_avi_to_mp4(avi_file_path, output_name):
    print('converting')
    os.system(
        "ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(
            input=avi_file_path, output=output_name))
    return True

def sendToTelegram( file_name):
    print('file_name', file_name)
    file = folder + "/" + file_name
    convert_avi_to_mp4(file, file)
    video = file + '.mp4'
    message = ('https://api.telegram.org/' + bot_token + '/sendDocument?chat_id=' + chat_id)
    send = requests.post(message, files={
        'document': open(video, 'rb')
    })
    print(send.status_code, send.reason, send.content)
    os.remove(file +'.mp4')

def main():
    if not os.path.exists('logs.txt'):
        open('logs.txt', 'w').close()
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    for file in onlyfiles:
        print(file)
        with open('logs.txt') as f:
            if file not in f.read():
                file1 = open("logs.txt", "a")
                file1.writelines(file)
                file1.close()
                print("file --", file)
                if file.endswith('.avi'):
                    sendToTelegram(file)


folder = '/working_dir'
bot_token='bot'+ os.environ['bot_token']
chat_id=os.environ['chat_id']
seconds = os.environ['interval']

schedule.every(seconds).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)