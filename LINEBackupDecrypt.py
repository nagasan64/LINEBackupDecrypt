import pathlib
import shutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

with open("./data/preCalc.bin", "rb") as f:
    preDatab = f.read()

encryptedZeroBytes = dict()
ind = 0
while ind < len(preDatab):
    encryptedZeroBytes[preDatab[ind+16:ind+32]] = preDatab[ind:ind+16]
    ind += 32

zipList = list(pathlib.Path("./LINE_Backup").glob("*.zip"))

for targetZipFile in zipList:
    chatID = str(targetZipFile.name).replace(".zip", "").replace("LINE_Android-backup-", "")
    print(chatID)

    try:
        shutil.unpack_archive(str(targetZipFile), "./output/" + chatID)
    except ValueError:
        continue
    
    for j in list(pathlib.Path("./output/" + chatID + "/linebackup/image").glob("*")):
        if not '.thumb' in str(j.name):
            j.rename(str(j) + ".jpg")

    with open("./output/" + chatID + "/linebackup/chat/" + chatID, "rb") as f:
        encryptedChat = f.read()

    with open("./output/" + chatID + "/linebackup/chat/" + chatID + ".extra", "r") as f:
        extraData = f.read()

    extraData = list(map(int, extraData.split(",")))
    zeroBytesSearch = [encryptedChat[0:16], encryptedChat[16:32], encryptedChat[32:48]]
    ind = 48
    while (not (zeroBytesSearch[0] == zeroBytesSearch[1] and zeroBytesSearch[0] == zeroBytesSearch[2])):
        zeroBytesSearch.pop(0)
        zeroBytesSearch.append(encryptedChat[ind:ind+16])
        ind += 16

    decryptedChat = b""
    cipher = AES.new(encryptedZeroBytes[zeroBytesSearch[0]],AES.MODE_ECB)
    ind = 0
    for j in extraData:
        decryptedChat += unpad(cipher.decrypt(encryptedChat[ind:ind+j]), 16)
        ind += j
    
    with open("./output/" + chatID + "/linebackup/chat/" + chatID + ".sqlite", "wb") as f:
        f.write(decryptedChat)

