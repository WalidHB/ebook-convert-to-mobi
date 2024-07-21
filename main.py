import cv2
from PIL import Image
from subprocess import Popen
import os
import glob


convert = True

# gets working directory so it works for you no matter the folder files are in
workdir = os.path.dirname(__file__)
imgs_list = []
rotate_landscape = True

ext = ['png', 'jpg', 'gif', 'jpeg', 'tiff']

for e in ext:
    imgs_list.extend(glob.glob(workdir + '/*.' + e))

imgs_list.sort()

resized = [None]*len(imgs_list)
im = [None]*len(imgs_list)


# setting dimensions of the file AFTER resize
dim = (2508, 3496)

for n in range(len(imgs_list)):

    # this is an opencv function for opening an image (in the same folder)
    img = cv2.imread(imgs_list[n])

    # turn to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    # rotating landscape images (optional you can just make this a False)
    if rotate_landscape:
        if img.shape[0]<img.shape[1]:
            print(img.shape)
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # preserving aspect ratio so no stretching happens
    dim0 = dim[0] / img.shape[1]
    dim1 = dim0 * img.shape[0]

    resize_dim = (dim[0] , int(dim1))


    # resize
    resized[n] = cv2.resize(img, resize_dim)

    # transforming the array to the image from bytes
    
    im[n] = Image.fromarray(resized[n])

pdf = im[0]
del im[0]

# saving the file as a pdf IN the working folder
pdf.save(workdir + '/file.pdf',save_all=True, append_images=im)


if convert:
    
    try:

        with open('file.mobi', 'wb') as out:
            
            #using calibre ebook-convert cli
            arg = ['ebook-convert', 'file.pdf', 'file.mobi']

            conversion = Popen(arg, stdout=out)
            
            #waiting for the conversion to finish
            conversion.wait()

    finally:
        # and finally kill the cmd process so we stop using the resources and then remove the temporary pdf file
        conversion.kill()
        os.remove(workdir + '/file.pdf')
