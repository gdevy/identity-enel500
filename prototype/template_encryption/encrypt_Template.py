from cryptography.fernet import Fernet
#key = Fernet.generate_key()
key = b'wWGAOCPMXdL2hcgllfjwz4fu0L_2gUtDMox36UiHNBw='

crypter = Fernet(key)

f = open("Output.txt", "w")

with open("crypto_Template.txt") as file:
    for line in file:
        decryptString = crypter.decrypt(str.encode(line.rstrip()[2:-1]))
#        print(str(decryptString, 'utf8'))
        f.write(str(decryptString, 'utf8'))
        f.write("\n")
file.close()
f.close()



