from instabot import Bot
import os, glob
import shutil
import json
import sys
import logging
import PySimpleGUI as sg
from PIL import Image, ImageTk
import io
import moviepy.editor as mp

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

with open('cerdentials.json') as json_data:
    cerdentials = json.load(json_data)


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

username = cerdentials['user']
password = cerdentials['password']
path = "posts"
#text = 'Rotating oscillating arcs' + '\r\n' + '#processing'

def file_is_video(f):
    return f.endswith(".mp4")

def file_is_foto(f):
    return f.endswith(".jpg")

def get_img_data(f, maxsize=(1200, 850), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format="GIF")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)


def get_img_caption(f):

    sg.theme('Dark Blue 3')  # please make your windows colorful

    event, values  = sg.Window('InstaUpload',
                        [[sg.Text("Caption for [%s]" % f)],
                            [sg.Image(key="-IMG-",data=get_img_data(f, first=True))],
#                            [sg.InputText()],
                            [sg.Multiline("\n\n#processing\n#creativecoding", size=(45,5))],
                            [sg.Submit(), sg.Cancel()]]).read(close=True)

    caption = values[0]     # the first input element is values[0]
    return caption

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info("on_created [%s]" % event.src_path)

        if( all(x not in event.src_path for x in ("THUMBNAIL", "CONVERTED"))) :
            clean_up(event.src_path)
            upload_post(event.src_path)

            logging.info("on_created : deleting [%s]" % event.src_path)
            for filename in glob.glob(event.src_path + "*"):
                os.remove(filename)

def clean_up(f):
    logging.info("clean_up()")
    if os.path.exists("config"):
        try:
            shutil.rmtree("config") # removing it because in 2021 it makes problems with new uploads
        except OSError as e:
            logging.error("Error: %s - %s." % (e.filename, e.strerror))
    if os.path.exists(f + ".REMOVE_ME"):
        src = os.path.realpath(f)
        os.rename(f + ".REMOVE_ME", src)

def upload_post(f):
    logging.info("upload_post()")

    if file_is_video(f):
        logging.info("generating thumbnail for video")
        vid = mp.VideoFileClip(f)
        thumbnail = "{fname}.THUMBNAIL.jpg".format(fname=f)
        vid.save_frame(thumbnail)
        vid.close()
    else :
        thumbnail = f

    logging.info("getting caption")
    caption = get_img_caption(thumbnail)
    logging.info("Caption = [%s]" % caption)

    bot = Bot()
    logging.info("bot.login(username=%s, password=%s)" % (username, password))
    bot.login(username=username, password=password, is_threaded=True)

    if file_is_foto(f) :
        logging.info("bot.upload_photo(mediafile=%s, caption=%s)" % (f, caption))
        bot.upload_photo(f, caption=caption)
    elif file_is_video(f):
        logging.info("bot.upload_video(mediafile=%s, thumbnail=%s, caption=%s)" % (f, thumbnail, caption))
        bot.upload_video(f, thumbnail=thumbnail, caption=caption)
    else:
        logging.info("not a video or foto (%s)" % f)

if __name__ == '__main__':

    event_handler = MyHandler()
    observer = Observer()
    logging.info("observer.schedule(event_handler, path=%s, recursive=False)" % path)
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
