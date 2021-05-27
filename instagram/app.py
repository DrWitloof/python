from instabot import Bot
import os
import shutil

username = 'koen@banaanmaan.be'
password = ''
mediafile = "posts/upload.mp4"
text = 'Rotating oscillating arcs' + '\r\n' + '#processing'

def clean_up():
    dir = "config"
    remove_me = mediafile + ".REMOVE_ME"
    # checking whether config folder exists or not
    if os.path.exists(dir):
        try:
            # removing it because in 2021 it makes problems with new uploads
            shutil.rmtree(dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    if os.path.exists(remove_me):
        src = os.path.realpath(mediafile)
        os.rename(remove_me, src)

def upload_post():
    bot = Bot()

    bot.login(username=username, password=password)
    if mediafile.endswith(('.mp4','.avi')):
        bot.upload_video(mediafile, caption=text)
    else:
        bot.upload_photo(mediafile, caption=text)


if __name__ == '__main__':
    clean_up()
    upload_post()
