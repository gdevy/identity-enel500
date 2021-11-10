from cryptography.fernet import Fernet

#key = Fernet.generate_key()

key = b'wWGAOCPMXdL2hcgllfjwz4fu0L_2gUtDMox36UiHNBw='

crypter = Fernet(key)



f = open("crypto_Template.txt", "w")

with open("Template.txt") as file:
    for line in file:
         x=crypter.encrypt(str.encode(line.rstrip()))
         f.write(str(x))
         f.write("\n")
file.close()
f.close()


