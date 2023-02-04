# LINEBackupDecrypt

過去のバージョンのAndroid版LINEアプリで出力できた、zip形式のトーク履歴(LINE_Android-backup-*.zip)を解凍・復号するPythonスクリプトです。出力形式は、トーク履歴がSQLITEデータベース(.sqlite)、写真がJPEG(.jpg)とサムネイル(.thumb)です。

This Python script decompresses and decrypts the zip format talk history (LINE_Android-backup-*.zip) that could be made with past versions of the Android LINE application. The output format is SQLITE database (.sqlite) for the talk history, and JPEG (.jpg) and thumbnail (.thumb) for the photos.

## Background
トーク履歴は、PKCS#7 paddingを使ったAES-256-ECBで暗号化されています。鍵はトーク履歴固有の文字列を、Javaの```String.hashCode()```にかけたものを、独自の関数で256bitに拡張しています。しかし、AES-256の鍵空間(2^256)に対して、```String.hashCode()```の出力の型は```int```(2^32)で、さらに独自の関数の出力はわずか22万通りしかありません。さらに、トーク履歴のSQLITEデータベースは0を連続して含む区間が多く存在するため、これを利用して鍵を特定することができます。

The talk history is encrypted with AES-256-ECB using PKCS#7 padding. The key is a talk history-specific string hashed by Java's ```String.hashCode()``` and extended to 256 bits with another function. However, the output type of ```String.hashCode()``` is ```int``` (2^32) for the AES-256 keyspace (2^256), and the output of the hash extension function has only about 220,000 possible values. Furthermore, the SQLITE database of talk history contains many intervals containing consecutive zeros, which can be used to identify the key.

## Usage
LINE_Backupにトーク履歴のzipファイルを入れ、LINEBackupDecrypt.pyのあるディレクトリで```python LINEBackupDecrypt.py```を実行してください。

Put the talk history zip file into LINE_Backup and run ```python LINEBackupDecrypt.py``` in the directory where LINEBackupDecrypt.py is located.
