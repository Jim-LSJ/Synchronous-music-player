# Embedded System Lab
###### tags: `ESLab` `Final Project`

## Objective
- 同步音響

## Device and Material
- Raspberry pi
- 音響

## Done

1. 預先處理音訊檔，把wav分成左右聲道，存成兩個wav

2. Server(電腦)開啟，client_left, client_right(兩台音響+rpi)連上線後，server按任意鍵即開始同步播放

## BUG
1. pygame播放時，速度會不穩，導致剛開始能同步，最後有可能不同步

    - 可能解法：
        1. pygame 1.9.2版有提供set_pos()設定播放時間，但是無法直接pip install此版本
        2. pygame.mixer.music.play(loop, start_pos)可以設定時間，但是目前不支援wav檔的設定，只支援mp3檔

## TODO
1. 新增stop, pause功能

2. 架構可能要改成音響當server，下指令的電腦當client。一旦Raspberry pi開機，就開啟server.py等待電腦連線，似乎比較符合真實情況的架構。


## 同步
1. rpi_1在t1時傳t1給rpi_2

2. rpi_2在t2時收到rpi_1傳來的t1，傳t2給rpi_1

3. rpi_1在t3時收到rpi_2傳來的t2，傳t3給rpi_2

4. rpi_2在t4時收到rpi_1傳來的t3

- 此時兩台rpi都知道round trip time = t3 - t1 = t4 - t2
- rpi_1主控時，傳訊息給rpi_2，讓rpi_2先開啟音響，rpi_1延遲一個round trip time 在開啟音響。

## Important!!
- Deadline: 6/11
- Code
- report
- demo video