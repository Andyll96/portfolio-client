import math

class Photo:
    def __init__(self, imagePath, myImage, albumName):
        self.fileName = imagePath[-12:]
        self.fileLocation = imagePath
        self.thumbnailLocation = ''
        self.albumName = albumName
        self.dateTaken = myImage.datetime_original
        self.fStop = myImage.f_number
        self.shutterSpeed =   '1/' + str(int(math.ceil(1000 / float(myImage.exposure_time * 1000))))
        self.iso = myImage.photographic_sensitivity
        self.focalLength = myImage.focal_length
        self.camera = myImage.model
        self.lens = myImage.lens_model


    def __str__(self):
        return '\tfileName: {self.fileName}\n\t\tfileLocation: {self.fileLocation}\n\t\tthumbnailLocation: {self.thumbnailLocation}\n\t\talbumName: {self.albumName}\n\t\tdateTaken: {self.dateTaken}\n\t\tfStop: {self.fStop}\n\t\tshutterSpeed: {self.shutterSpeed}\n\t\tiso: {self.iso}\n\t\tfocalLength: {self.focalLength}\n\t\tcamera: {self.camera}\n\t\tlens: {self.lens}'.format(self=self)