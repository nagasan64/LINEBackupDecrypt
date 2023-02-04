import pathlib
import shutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

with open("./data/preCalc.bin", "rb") as f:
    preDatab = f.read()

preData = dict()
ind = 0
while ind < len(preDatab):
    preData[preDatab[ind+16:ind+32]] = preDatab[ind:ind+16]
    ind += 32

zipList = list(pathlib.Path("./LINE_Backup").glob("*.zip"))

for i in zipList:
    fileName = str(i.name).replace(".zip", "").replace("LINE_Android-backup-", "")
    print(fileName)
    try:
        shutil.unpack_archive(str(i), "./output/" + fileName)
    except ValueError:
        continue
    
    for j in list(pathlib.Path("./output/" + fileName + "/linebackup/image").glob("*")):
        if not '.thumb' in str(j.name):
            j.rename(str(j) + ".jpg")

    with open("./output/" + fileName + "/linebackup/chat/" + fileName, "rb") as f:
        encryptedChat = f.read()

    with open("./output/" + fileName + "/linebackup/chat/" + fileName + ".extra", "r") as f:
        extraData = f.read()

    extraData = list(map(int, extraData.split(",")))
    decryptedChat = b""
    zeroBytesList = [encryptedChat[0:16], encryptedChat[16:32], encryptedChat[32:48]]
    ind = 48
    while (not (zeroBytesList[0] == zeroBytesList[1] and zeroBytesList[0] == zeroBytesList[2])):
        zeroBytesList.pop(0)
        zeroBytesList.append(encryptedChat[ind:ind+16])
        ind += 16

    for j in preData.keys():
        if j[:2] == "64":
            print(j)
    cipher = AES.new(preData[zeroBytesList[0]],AES.MODE_ECB)
    ind = 0
    for j in extraData:
        #print(cipher.decrypt(encryptedChat[ind:ind+j]))
        decryptedChat += unpad(cipher.decrypt(encryptedChat[ind:ind+j]), 16)
        ind += j
    
    with open("./output/" + fileName + "/linebackup/chat/" + fileName + ".sqlite", "wb") as f:
        f.write(decryptedChat)

