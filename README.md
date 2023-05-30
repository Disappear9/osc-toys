# OSC-Toys

[中文](https://github.com/Sakura0721/osc-toys/blob/master/README_ZH.md)

This project integrates bluetooth toys to VRChat avatars using OSC.

## Supported Toys

- DG-Lab E-Stim

## Supported Games

- VRChat (you must have an avatar supporting OSC with suitable avatar parameters)

## How does it work?

This program will communicate with VRChat using [OSC](https://docs.vrchat.com/docs/osc-overview).

It will listen to some values from VRC, and change the strength of toys.

For example, with this program, you can implement effects like when someone touch ears of your avatar, you will get shocked.

## Setup and Installation

- Clone this repo and install dependences.

```bash
git clone https://github.com/Sakura0721/osc-toys.git
cd osc-toy
pip install -r requirements.txt
```

- Edit settings.py, fill in necessary fields.
  - `COYOTE_UID`: If you don't know what it is, just set `COYOTE_UID = None`, the program will try to detact your device automatically.
  - `COYOTE_SAFE_MODE`: Enable or disable safe mode. This caps the max e-stim output of the device. Warning: Don't touch unless you know what you're doing!
  - `COYOTE_MAX_POWER`: Output power of Coyote when the value from VSC equals to `1.0`.
  - `COYOTE_PATTERN`: Output pattern of Coyote. See `data\estim\pattern_dict.json`.
  - `COYOTE_ADDR_A` and `COYOTE_ADDR_B`: OSC address bind to channel A/B.
  - `VRC_HOST` and `VRC_OSC_PORT`: OSC ip address and port of VRC. If you have no idea what it is, leave it as default.
- Find an avatar supports [OSC](https://docs.vrchat.com/docs/osc-overview) parameters, such as avatars enabled [VRCContactReceiver](https://docs.vrchat.com/docs/contacts#vrccontactreceiver).
  - Note that the parameters should be `float`. I.e. [Proximity](https://docs.vrchat.com/docs/contacts#receiver) reveiver type.
  - If you don't know what it is, find a modeler/avatar-creater to help you.
- Start VRC, and then run `main.py`. Enjoy it with your partner!

```bash
python main.py
```

## Changing Patterns

TBD: Better documentation here.

E-stim patterns are listed under the `data/estim/pattern_dict.json` file, and the `data/estim/patterns/` folder.

## Troubleshooting

If the program faild to connect to Coyote, try re-run it or re-run it after reboot bluetooth of your computer.

## Todos

- [ ] Add more toys.
  - If you have any toys want to be supported, welcome to open an issue or a PR.
- [ ] Tidy up the code, add more comments.
  - I know it's a mess, but I'm too lazy to fix it.
- [ ] Support GUI.
  - I don't like GUI, I think it works fine with command line for now.

## Acknowledgements

- Code of communication with Coyote is based on [GIFT](https://github.com/MinLL/GameInterfaceForToys). Thanks to [@MinLL](https://www.github.com/MinLL) and [@inertaert](https://github.com/inertaert).
