# OSC-Toys

该项目使用 OSC 将蓝牙玩具集成到 VRChat Avatar 中。

## 支持的玩具

- DG-Lab E-Stim（郊狼）

## 支持的游戏

- VRChat（您必须拥有一个支持 OSC 的、具有适当 Avatar 参数的模型）

## 如何工作

该程序将使用 [OSC](https://docs.vrchat.com/docs/osc-overview) 与 VRChat 通信。

它将监听 VRC 发送的某些数值，并更改玩具的力度（例如郊狼的电击强度）。

例如，使用此程序，您可以实现当某人触摸您的 Avatar 的耳朵时，您将受到电击的效果。

## 设置和安装

- 克隆此仓库并安装依赖项。

```bash
git clone https://github.com/Sakura0721/osc-toys.git
cd osc-toy
pip install -r requirements.txt
```

- 编辑`settings.py`并填写必要字段。
  - `COYOTE_UID` ：如果您不知道它是什么，请设置 `COYOTE_UID = None` ，程序将自动尝试检测您的设备。
  - `COYOTE_SAFE_MODE` ：启用或禁用安全模式。这会限制设备的最大电刺激输出。警告：如果你不知道你在做什么，将这个值设置为 True。
  - `COYOTE_MAX_POWER` ：当来自 VSC 的值等于 1.0 时，郊狼的输出强度。
  - `COYOTE_PATTERN` ：`Coyote` 的输出模式。 请参见`data\estim\pattern_dict.json`。
  - `COYOTE_ADDR_A` 和 `COYOTE_ADDR_B` ：绑定到通道 A/B 的 OSC 地址。
  - `VRC_HOST` 和 `VRC_OSC_PORT` ：VRC 的 OSC IP 地址和端口。如果您不知道它是什么，请将其保留为默认值。
- 找到一个支持 OSC 参数的 Avatar，例如使用了 [VRCContactReceiver](https://docs.vrchat.com/docs/contacts#vrccontactreceiver) 的 Avatar。
  - 需要注意参数类型应该为 `float`。即需要使用类型为 [Proximity](https://docs.vrchat.com/docs/contacts#receiver) 的 reveiver.
  - 如果您不知道这是什么，请找一个模型师/Avatar 创作者来帮助您。
- 启动 VRC，然后运行 main.py。与您的搭档一起享受吧！

```bash
python main.py
```

## 更改波形

TODO：更好的文档。
郊狼波形当前存储在 `data/vibrators/pattern_dict.json` 下，子波形在 `data/estim/patterns/` 文件夹下。

## 故障排除

如果程序无法连接到郊狼，请尝试重新运行它；如果仍然无法连接，在计算机上重启蓝牙后再重新运行。

## Todos

- [ ] 增加更多玩具
  - 如果你有需求，欢迎开 issue 或 PR
- [ ] 整理代码,添加注释
  - 代码有点乱，但是能跑，暂时懒得改
- [ ] 支持 GUI
  - 不喜欢 GUI，目前能用，必要的时候再考虑
