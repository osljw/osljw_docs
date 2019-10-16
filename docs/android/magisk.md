

# bootloader
进入bootloader模式, `-s`参数用于指定设备, 可以通过`adb devices`命令获得
```
adb -s b860fe37 reboot bootloader
```

# recovery
音量+键和电源键同时按住，持续3秒后松开

TWRP https://twrp.me/

# magisk
https://topjohnwu.github.io/Magisk/



# xiaomi
ROM https://xiaomifirmwareupdater.com/miui/libra/

Kernel https://github.com/MiCode/Xiaomi_Kernel_OpenSource


# linux deploy

https://github.com/meefik/linuxdeploy

ssh登陆, 密码可以在配置中找到
```
ssh android@<ip>
```

ssh连接后切换到root
```
sudo su
```