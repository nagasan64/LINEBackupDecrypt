# LINEBackupDecrypt

過去のバージョンのAndroid版LINEアプリで出力できた、zip形式のトーク履歴(LINE_Android-backup-*.zip)を解凍・復号するPythonスクリプトです。出力形式は、トーク履歴がSQLITEデータベース(.sqlite)、写真がJPEG(.jpg)とサムネイル(.thumb)です。

This Python script unzips and decrypts the LINE Android backup files in the zip format (LINE_Android-backup-*.zip) created by older versions of the Android LINE app. The resulting output is in the form of SQLITE database (.sqlite) for chat history and JPEG (.jpg) and thumbnail (.thumb) for photos.


手元にあったサンプルが少ないため、バックアップしたバージョンによっては暗号化方式が異なる場合があります。

Note that the encryption method may vary depending on the version of the backup, as I only had a limited number of samples available.

## Background
トーク履歴は、PKCS#7 paddingを使ったAES-256-ECBで暗号化されています。鍵はトーク履歴固有の文字列を、Javaの```String.hashCode()```にかけたものを、独自の関数で256bitに拡張しています。しかし、AES-256の鍵空間(2^256)に対して、```String.hashCode()```の出力の型は```int```(2^32)で、さらに独自の関数の出力はわずか22万通りしかありません。また、トーク履歴のSQLITEデータベースは0を連続して含む区間が多く存在するため、これを利用して鍵を特定することができます。

The chat history is encrypted using AES-256-ECB and PKCS#7 padding. The encryption key is derived from a history-specific string hashed by Java's ```String.hashCode()``` method, and then expanded to 256 bits with another function. However, the output of ```String.hashCode()``` is an ```int``` (2^32), which is much smaller than the AES-256 keyspace (2^256), and the output of the hash extension function has limited possible values (around 220,000). Additionally, the SQLITE database of the chat history has many intervals with consecutive zeros, which can be used to identify the key.

## Usage
LINE_Backupにトーク履歴のzipファイルを入れ、LINEBackupDecrypt.pyのあるディレクトリで```python LINEBackupDecrypt.py```を実行してください。

To use this script, place the chat history zip file into the "LINE_Backup" folder, and then run ```python LINEBackupDecrypt.py``` in the directory where the ```LINEBackupDecrypt.py``` script is located.
