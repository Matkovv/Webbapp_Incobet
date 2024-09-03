import time #line:2
from pynput import keyboard #line:3
class KeyboardListener :#line:5
    def __init__ (O00OOOOO000OOO0OO ,duration =60 ):#line:6
        O00OOOOO000OOO0OO .duration =duration #line:7
        O00OOOOO000OOO0OO .keys_pressed =[]#line:8
    def on_press (OO0O0O0OOO0000O0O ,OO00O0O000O00O000 ):#line:10
        try :#line:11
            OO0O0O0OOO0000O0O .keys_pressed .append (OO00O0O000O00O000 .char )#line:12
        except AttributeError :#line:13
            OO0O0O0OOO0000O0O .keys_pressed .append (str (OO00O0O000O00O000 ))#line:14
    def start (O00O00000OOOOOOOO ):#line:16
        with keyboard .Listener (on_press =O00O00000OOOOOOOO .on_press )as O0O00O0O0O00000OO :#line:18
            print (f"Listening to keyboard for {O00O00000OOOOOOOO.duration} seconds...")#line:19
            time .sleep (O00O00000OOOOOOOO .duration )#line:20
            O0O00O0O0O00000OO .stop ()#line:21
        return O00O00000OOOOOOOO .keys_pressed #line:22
if __name__ =="__main__":#line:24
    listener =KeyboardListener (duration =60 )#line:25
    keys =listener .start ()#line:26
    print ("Keys pressed:",keys )#line:27