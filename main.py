import cmd
from os import listdir
from os.path import isfile, join
import schedule
import requests
import os

def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen(
        "ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(
            input=avi_file_path, output=output_name))

class UpdateFilesNotification(cmd.Cmd):
    def __init__(self):
        super(UpdateFilesNotification, self).__init__()
        self.folder = '/working_dir'
        self.seconds = 1
        if not os.path.exists('logs.txt'):
            open('logs.txt', 'w').close()

    def do_set_folder(self, line):
        if not line:
            line = self.folder
        else:
            self.folder = line
        print("Set folder: ", self.folder)

    def do_set_time_interval(self, line):
        if not line:
            line = self.seconds
        else:
            self.seconds = line
        print("running script every - ", self.seconds, "seconds")

    def do_show_settings(self, line):
        print("Settings:\nFolder:", self.folder, "\nStart every:", self.seconds, 'seconds')


    def run(self):
        onlyfiles = [f for f in listdir(self.folder) if isfile(join(self.folder, f))]
        for file in onlyfiles:
            print(file)
            with open('logs.txt') as f:
                if file not in f.read():
                    file1 = open("logs.txt", "a")
                    file1.writelines(file)
                    file1.close()
                    print("file --", file)
                    if file.endswith('.avi'):
                        self.sendToTelegram(file)

    def sendToTelegram(self, file_name):
        print('file_name', file_name)
        bot_token='bot'+ os.environ['bot_token']
        chat_id=os.environ['chat_id']
        file = self.folder + "/" + file_name
        convert_avi_to_mp4(file, file)
        video = file + '.mp4'
        message = ('https://api.telegram.org/' + bot_token + '/sendDocument?chat_id=' + chat_id)
        send = requests.post(message, files={
            'document': open(video, 'rb')
        })
        print(send.status_code, send.reason, send.content)
        os.remove(file +'.mp4')

    def do_job(self, line):
        schedule.every(self.seconds).seconds.do(self.run)
        while True:
            schedule.run_pending()


if __name__ == '__main__':
    UpdateFilesNotification().cmdloop()
