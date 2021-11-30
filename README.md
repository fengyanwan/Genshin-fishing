<h1 align="center">Genshin-fishing</h1>
<p align="center">
    <img src="https://img.shields.io/github/last-commit/fengyanwan/Genshin-fishing">
    <img src="https://img.shields.io/github/languages/top/fengyanwan/Genshin-fishing">
</p>

## function now 现在能使用的功能：

auto pull fishing rod in genshin game.  
在原神游戏中钓鱼时自动拉钓鱼竿。

## 1.Module requirements 依赖模块

* build in module 内置模块：time
* out module 外部模块: OpenCV、numpy、pywin32、Pillow

## 2.Testing environment 测试环境

* computer：HP OMEN 15 laptop
* OS：windows 10 21H1 (19043.1348)
* saftware：PyCharm 2021.2.3 (Community Efition) Administrator mode
* screen size: 1920 × 1080
* game：genshin_impact 2.3

## 3.Principle 实现原理

1. use pillow module to screenshot. 使用pillow模块对全屏截图。
2. OpenCV match the img on the screenshot,locate the image center. 利用opencv匹配目标图片，找出图片的中心位置。
3. calculate the distance between the cursor and the range center. 计算光标与正确范围的距离。
4. Press the mouse according to the distance. 根据距离按下鼠标。
