import face_recognition
from cryptography.fernet import Fernet

key = b'wWGAOCPMXdL2hcgllfjwz4fu0L_2gUtDMox36UiHNBw='
crypter = Fernet(key)
image1=face_recognition.load_image_file("T.jpeg")
image1_face_encoding=face_recognition.face_encodings(image1)[0]
print(image1_face_encoding)
file1 = open("T.txt","w")
i=0
while(i<128):
    file1.write(str(image1_face_encoding[i])+'\n')
#    file1.write(str(crypter.encrypt(str.encode(str(image1_face_encoding[i]))))[2:-1]+'\n')
    i=i+1
file1.close()
