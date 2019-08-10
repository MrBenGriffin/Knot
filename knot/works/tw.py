from enum import IntFlag


class Tw(IntFlag):
    master = 0x0000
    horizon = 0x0001  # HMirror
    vanity = 0x0002   # VMirror
    mirror = 0x0003
    rot000 = 0x0004  # rotate 0
    rot090 = 0x0005  #
    rot270 = 0x0006  #
    rot180 = 0x0007  #
