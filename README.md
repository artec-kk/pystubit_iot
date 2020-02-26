# ArtecRobo2.0 IoT用 MicroPython ライブラリ

## 本ソフトウェア
本ソフトウェアは、株式会社アーテックが開発・販売しておりますロボットプログラミング教材"ArtecRobo2.0"を制御するMicroPython用ライブラリのソースコードです。

## 対応OS
[StuduinoBit_MicroPython](https://github.com/artec-kk/StuduinoBit_MicroPython)

## フィードバックについて
本ソフトウェアに対するご指摘、改善要望については [Issues](/issues) へお願いいたします。

## ライセンスと免責事項
MIT

## インストール方法
MicroPython配布パッケージ [micropython-studuinobit-iot](https://pypi.org/project/micropython-studuinobit-iot/)で配布しています。upipパッケージマネージャを使用してインストールする方法を下記に記します。

### ネットワーク接続
StuduinoBit_MicroPythonのREPLで下記のように実行し、インターネットに繋がっているWiFiと接続してください。

`>>> import network`<br>
`>>> sta = network.WLAN(network.STA_IF)`<br>
`>>> sta.active(True)`<br>
`>>> sta.connect("SSID", "PASSWORD")`<br>

※"SSID"と"PASSWORD"は、使用される環境に合わせて設定してください。

### ライブラリのインストール

`>>> import upip`<br>
`>>> upip.install("micropython-studuinobit-iot")`<br>

## 使い方

ロボット拡張ユニット用リファレンス 参照 (現在作成中)

## Author
[Artec Co., Ltd. Development team](https://github.com/artec-kk)  
[Artec Co., Ltd.](http://www.artec-kk.co.jp)  
