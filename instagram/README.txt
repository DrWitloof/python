Starting from https://www.youtube.com/watch?v=vnfhv1E1dU4

https://github.com/ohld/igbot/blob/master/instabot/bot/bot.py

https://stackoverflow.com/questions/62293200/upload-images-to-instagram-using-python

# video
    def upload_video(self, video, caption="", thumbnail=None, options={}):
        """Upload video to Instagram
        @param video      Path to video file (String)
        @param caption    Media description (String)
        @param thumbnail  Path to thumbnail for video (String). When None,
                          then thumbnail is generated automatically
        @param options    Object with difference options, e.g.
                          configure_timeout, rename_thumbnail, rename (Dict)
                          Designed to reduce the number of function arguments!
        @return           Object with Instagram upload state (or False)
        """
