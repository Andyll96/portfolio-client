from datetime import date
class Album:
    def __init__(self):
        self.title = input('Album Title: ')
        self.date = ''
        self.uploadDate = date.today()
        self.photoCount = 0.0
        self.description = input('Album Description: ')
        self.photos = []

    def __str__(self):
        return 'Album Title: {self.title}\nAlbum Date: {self.date}\nAlbum Upload Date: {self.uploadDate}\nAlbumPhotoCount: {self.photoCount}\nAlbum Description: {self.description}'.format(self=self)