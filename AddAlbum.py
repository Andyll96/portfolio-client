from Album import Album
from Photo import Photo
import tkinter as tk
import tkinter.filedialog as fd
from exif import Image
from pymongo import MongoClient

MONGOURL = 'mongodb+srv://allactah:Al%23416587@portfolio-cluster.okbvf.mongodb.net/portfolio-database?retryWrites=true&w=majority'

def openFiles(root, title):
    """Opens file explorer to select photos

    Args:
        root ([type]): Needed in order to open file explorer
        title ([type]): Title / prompt for title bar of file explorer

    Returns:
        Tuple: Selected images
    """
    files = fd.askopenfilenames(parent = root, title = title)
    return files

def outputPrint():
    """Prints out album object and photos
    """
    print('---------------------------------OUTPUT---------------------------------')
    print(newAlbum)
    for photo in newAlbum.photos:
        print(photo)
    print('---------------------------------OUTPUT---------------------------------')

def mongoSetup():
    """Sets up MongoDB Client in order to communicate with MongoDB 

    Returns:
        List: A list of multiple objects needed to reference collections in the MongoDB 
    """
    client = MongoClient(MONGOURL)
    db = client.get_default_database()
    albums = db.albums
    images = db.images
    ObjectIDs = []

    return client, db, albums, images, ObjectIDs

root = tk.Tk()
fullResFiles = openFiles(root, 'Choose Original Photos')
thumbFiles = openFiles(root, 'Choose Thumbnail Photos')

newAlbum = Album()

# loops through full resolution files
for imagePath in fullResFiles:
    # with each imagePath open the photo and create a Photo Object
    with open(imagePath, 'rb') as image_file:
        myImage = Image(image_file)
        newPhoto = Photo(imagePath, myImage, newAlbum.title)

        # update album date and add photo to album data structure
        newAlbum.date = myImage.datetime_original[:10]
        newAlbum.photos.append(newPhoto)
        newAlbum.photoCount += 1

# loops through thumbnmail files
for thumbPath in thumbFiles:
    with open(thumbPath, 'rb') as thumb_file:
        # loop through full res images in the album and if the image and the thumbnail match, add the thumbnail path to the image
        for image in newAlbum.photos:
            if image.fileName == thumbPath[-12:]:
                image.thumbnailLocation = thumbPath

outputPrint()

client, db, albums, images, ObjectIDs = mongoSetup()

#inserts images into database
for image in newAlbum.photos:
    imageObject = {
        "fileName" : image.fileName,
        "fileLocation": "/img/photos/" + image.fileName,
        "thumbLocation": "/img/photos/thumbs/" + image.fileName,
        "albumName": image.albumName,
        "dateTaken": image.dateTaken,
        "fStop": image.fStop,
        "shutterSpeed": image.shutterSpeed,
        "iso": image.iso,
        "focalLength": image.focalLength,
        "camera": image.camera,
        "lens": image.lens
    }

    insertedID = images.insert_one(imageObject).inserted_id
    ObjectIDs.append(insertedID)
    albums.update_one({"title": "All Photos"}, {"$push":{"images": insertedID}})
    albums.update_one({"title": "All Photos"}, {"$inc": {"photoCount": 1}})

albumObject = {
    "title": newAlbum.title,
    # "dateTaken": newAlbum.date,
    # "uploadDate":newAlbum.uploadDate,
    "photoCount": newAlbum.photoCount,
    "description": newAlbum.description,
    "images": ObjectIDs
}
albums.insert_one(albumObject)
