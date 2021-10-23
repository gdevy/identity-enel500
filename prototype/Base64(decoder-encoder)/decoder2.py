import base64

file = 'zoom.jpg'
out_file = 'zoom.dat'

with open(file, 'rb') as image:
    image_read = image.read()

image_64_encode = base64.encodebytes(image_read)
image_64_decode = base64.decodebytes(image_64_encode)

with open(out_file, 'wb') as f:
    f.write(image_64_decode)
