

# init
pid=1

System V init

# systemd
systemd – A init replacement daemon designed to start process in parallel, implemented in a number of standard distribution – Fedora, OpenSuSE, Arch, RHEL, CentOS, etc.

debian系统
```
$ ls -l /sbin/init
/sbin/init -> /lib/systemd/systemd
```

# android init
rc脚本 https://android.googlesource.com/platform/system/core/+/master/init/README.md


init.qcom.rc
```
service wpa_supplicant /system/bin/wpa_supplicant \
    -iwlan0 -Dnl80211 -c/data/misc/wifi/wpa_supplicant.conf \
    -I/system/etc/wifi/wpa_supplicant_overlay.conf \
    -O/data/misc/wifi/sockets -dd \
    -e/data/misc/wifi/entropy.bin -g@android:wpa_wlan0
    #   we will start as root and wpa_supplicant will switch to user wifi
    #   after setting up the capabilities required for WEXT
    #   user wifi
    #   group wifi inet keystore
    class main
    socket wpa_wlan0 dgram 660 wifi wifi
    disabled
    oneshot

service p2p_supplicant /system/bin/wpa_supplicant \
    -ip2p0 -Dnl80211 -c/data/misc/wifi/p2p_supplicant.conf \
    -I/system/etc/wifi/p2p_supplicant_overlay.conf -N \
    -iwlan0 -Dnl80211 -c/data/misc/wifi/wpa_supplicant.conf \
    -I/system/etc/wifi/wpa_supplicant_overlay.conf \
    -O/data/misc/wifi/sockets -puse_p2p_group_interface=1 -dd \
    -e/data/misc/wifi/entropy.bin -g@android:wpa_wlan0
#   we will start as root and wpa_supplicant will switch to user wifi
#   after setting up the capabilities required for WEXT
#   user wifi
#   group wifi inet keystore
    class main
    socket wpa_wlan0 dgram 660 wifi wifi
    disabled
    oneshot
```

init.rc中多处存在class_start，负责启动属于main类型的service
```
class_start main
```

停止服务, usb连接，adb shell后，切换到root用户
```
setprop ctl.stop wpa_supplicant
setprop ctl.stop p2p_supplicant
```

查询服务状态
```
getprop | grep wpa_supplicant
```


重新挂载根文件系统为可读写
```
mount -o rw,remount /
```

查看设备分区
```
cat /proc/partitions

ls -l /dev/block/platform/soc.0/f9824900.sdhci/by-name/

mount 
df -h
```

boot分区和recovery分区各自包含自己的kernel和rootfs

boot分区
```
# ls -l /dev/block/platform/soc.0/f9824900.sdhci/by-name/boot

lrwxrwxrwx 1 root root 21 2019-10-17 09:37 /dev/block/platform/soc.0/f9824900.sdhci/by-name/boot -> /dev/block/mmcblk0p37
```
查看block设备的大小
- `cat /proc/partitions`命令输出blocks的个数, block的大小为1024 bytes
- `blockdev --getsize64 /dev/sda` returns size in bytes
- `cat /sys/class/block/mmcblk0p37/size` size in 512-byte blocks
- `fdisk -l /dev/block/mmcblk0`


android boot.img
- kernel
- ramdisk(rootfs)
- second stage(dtb)