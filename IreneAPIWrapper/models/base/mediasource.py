from . import File


class MediaSource(File):
    def __init__(self, url, file_type=None):
        # TODO: file location
        super(MediaSource, self).__init__(file_type=file_type)
        self.url = url
