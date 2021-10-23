import base64

with open("data.dat", "rb") as f:
    text = f.read()

image_64_encode = base64.encodebytes(text)
image_64_decode = base64.decodebytes(image_64_encode)

with open('datadat.txt', 'wb') as image_result:
    image_result.write(image_64_decode)
