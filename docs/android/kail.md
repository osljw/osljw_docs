
# kail linux on android
https://forum.xda-developers.com/android/general/kali-linux-android-phone-metasploit-t3057423


使用pc可以同时访问手机的chroot shell和 adb shell，
- usb连接，调试模式， 可以访问adb shell
- usb共享网络，或者手机与pc处于联通网络下，通过ssh访问kail的shell

# 挂载android分区
在kail linux的shell中

查看android分区情况
```
ls -l /dev/block/bootdevice/by-name/
```

查看设备分区，大小和文件系统类型, 文件系统类型为unknown的不可以挂载
``
fdisk -l /dev/block/mmcblk0
``

挂载android分区到kail linux环境中
```
mkdir /android_system
mount /dev/block/bootdevice/by-name/system /android_system
```

# aircrack-ng
```
sudo apt-get install -y aircrack-ng
apt-get install pciutils
```

monitor mode 和 managed mode
```
# 查看网卡芯片类型
lspci
lsusb
```

确认网卡和驱动是否支持monitor mode
https://www.aircrack-ng.org/doku.php?id=compatibility_drivers


reaver pin
https://klionsec.github.io/2015/04/16/reaver-crack-pin-code/#menu