import time
import board
# 'A0', 'A1', 'A2', 'A3', 'GP0', 'GP1', 'GP10', 'GP11', 'GP12', 'GP13', 'GP14', 'GP15', 'GP16', 'GP17', 'GP18', 'GP19', 'GP2', 'GP20', 'GP21', 'GP22', 'GP26',
# 'GP26_A0', 'GP27', 'GP27_A1', 'GP28', 'GP28_A2', 'GP3', 'GP4', 'GP5', 'GP6', 'GP7', 'GP8', 'GP9', 'LED', 'SMPS_MODE', 'STEMMA_I2C', 'VBUS_SENSE', 'VOLTAGE_MONITOR', 'board_id'
import digitalio
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from hid_gamepad import Gamepad

class Button:
    def __init__(self, io, name, num=None):
        self.io = io
        self.name = name
        self.state = False
        if num is not None:
            self.num = num

buttons = {}

up = DigitalInOut(board.GP0)
up.direction = Direction.INPUT
up.pull = Pull.UP
buttons['up'] = Button(up, 'up')

lk = DigitalInOut(board.GP1)
lk.direction = Direction.INPUT
lk.pull = Pull.UP
buttons['lk'] = Button(lk, 'lk', 4)

mk = DigitalInOut(board.GP2)
mk.direction = Direction.INPUT
mk.pull = Pull.UP
buttons['mk'] = Button(mk, 'mk', 5)

hk = DigitalInOut(board.GP3)
hk.direction = Direction.INPUT
hk.pull = Pull.UP
buttons['hk'] = Button(hk, 'hk', 6)

kkk = DigitalInOut(board.GP4)
kkk.direction = Direction.INPUT
kkk.pull = Pull.UP
buttons['kkk'] = Button(kkk, 'kkk', 7)

ppp = DigitalInOut(board.GP5)
ppp.direction = Direction.INPUT
ppp.pull = Pull.UP
buttons['ppp'] = Button(ppp, 'ppp', 3)

hp = DigitalInOut(board.GP6)
hp.direction = Direction.INPUT
hp.pull = Pull.UP
buttons['hp'] = Button(hp, 'hp', 2)

mp = DigitalInOut(board.GP7)
mp.direction = Direction.INPUT
mp.pull = Pull.UP
buttons['mp'] = Button(mp, 'mp', 1)

lp = DigitalInOut(board.GP8)
lp.direction = Direction.INPUT
lp.pull = Pull.UP
buttons['lp'] = Button(lp, 'lp', 0)

right = DigitalInOut(board.GP9)
right.direction = Direction.INPUT
right.pull = Pull.UP
buttons['right'] = Button(right, 'right')

down = DigitalInOut(board.GP10)
down.direction = Direction.INPUT
down.pull = Pull.UP
buttons['down'] = Button(down, 'down')

left = DigitalInOut(board.GP12)
left.direction = Direction.INPUT
left.pull = Pull.UP
buttons['left'] = Button(left, 'left')

start = DigitalInOut(board.GP18)
start.direction = Direction.INPUT
start.pull = Pull.UP
buttons['start'] = Button(start, 'start', 8)

select = DigitalInOut(board.GP17)
select.direction = Direction.INPUT
select.pull = Pull.UP
buttons['select'] = Button(select, 'select', 9)

facebuttons = [ buttons['lp'], buttons['mp'], buttons['hp'], buttons['ppp'], buttons['lk'], buttons['mk'], buttons['hk'], buttons['kkk'], buttons['start'], buttons['select'] ]
directions = [ buttons['up'], buttons['down'], buttons['left'], buttons['right'] ]

direction_mode = 0 # 0 is sticks, 1 is buttons (not implemented), 2 is directional hat/dpad (not implemented)

g = Gamepad(usb_hid.devices)

while True:
    dir_x = 0
    dir_y = 0

    # pressed = {'lp':False, 'mp':False, 'hp':False, 'ppp':False,
                # 'lk':False, 'mk':False, 'hk':False, 'kkk':False,
                # 'up':False, 'down':False, 'left':False, 'right':False,
                # 'start':False, 'select':False}

    for button in buttons.values():
        button.state = not button.io.value
        # if not buttons[key].io.value:
            # buttons[key].state = True

    #SOCD
    if buttons['up'].state and buttons['down'].state:
        buttons['up'].state = False
        buttons['down'].state = False
    if buttons['left'].state and buttons['right'].state:
        buttons['left'].state = False
        buttons['right'].state = False

    if direction_mode == 2:
        if buttons['up'].state and buttons['left'].state:
            #press up.left
            pass
        elif buttons['up'].state and buttons['right'].state:
            #press up.right
            pass
        elif buttons['down'].state and buttons['left'].state:
            #press down.left
            pass
        elif buttons['down'].state and buttons['right'].state:
            #press down.right
            pass
        elif buttons['up'].state:
            #press up
            pass
        elif buttons['down'].state:
            #press down
            pass
        elif buttons['left'].state:
            #press left
            pass
        elif buttons['right'].state:
            #press right
            pass
    else:
        if buttons['up'].state:
            dir_y = -127
        elif buttons['down'].state:
            dir_y = 127
        if buttons['left'].state:
            dir_x = -127
        elif buttons['right'].state:
            dir_x = 127
        g.move_joysticks(dir_x, dir_y)

    for button in facebuttons:
        if button.state:
            g.press_buttons(button.num + 1)
        elif not button.state:
            g.release_buttons(button.num + 1)

    time.sleep(0.01) # sleep for debounce
