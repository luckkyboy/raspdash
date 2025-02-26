[English](README.md) · __简体中文__

---

> [!NOTE]  
> 数字字体和文泉驿字体可以更换，但你需要调整文字的位置
> 
> 推荐安装ntp服务，确保开机通过网络加载时间。
> 
> 可以在start.sh中增加校准命令:
> 
> sudo ntpd -s -d


### 数据采集使用Raspberry Pi通过蓝牙连接OBD实现
#### 效果图
![image.png](dash/image.png)

> [!NOTE]  
> 如果你想查看具体视频，请点击 [Video.mp4](Video.mp4)

# 零件清单
- Raspberry pi 3B+
- 微雪 3.5inch RPi LCD (B)
- TF卡
- 支架（可选）

# 1. 通过树莓派蓝牙连接到OBD
### 替换 your_bluetooth_mac_address 为你OBD蓝牙的mac地址
#### 命令行下执行以下命令：
- bluetoothctl
  - power on
  - agent on
  - scan on
  - pair your_bluetooth_mac_address
  - trust your_bluetooth_mac_address
  - scan off
  - quit

[//]: # (# 2. 通过screen和/dev/rfcomm0交互（可选）)

[//]: # (### apt install screen)

[//]: # (命令行下执行以下命令：)

[//]: # (- screen /dev/rfcomm0)

[//]: # (  - ate0  <-- return ok)

[//]: # (  - atz)

[//]: # (  - atl1)

[//]: # (  - ath1)

[//]: # (  - atsp0  <-- use protocol auto, available protocols: 1,2,3,4,5,6,7,8,9,A)

[//]: # (  - 0100  <-- mode 01, pid 00, supported pids)

# 2. 安装脚本到树莓派
- 刷写raspberry os bullseye with desktop 64位
- 连接到网络，命令行执行以下命令
  - bash <(curl -ls https://raw.githubusercontent.com/luckkyboy/raspdash/refs/heads/main/install.sh)
- 在 ~/dash/start.sh 文件中替换 your_bluetooth_mac_address 为你的OBD蓝牙mac地址
- 重启到桌面，会自动打开terminal并运行相应程序!

# 历史记录
- 2025-02-26
  - 增加一言: v1.hitokoto.cn
  - 更改数字字体