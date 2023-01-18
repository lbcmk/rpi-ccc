import RPi.GPIO as GPIO
from time import sleep, time

GPIO.setmode(GPIO.BCM)

GPIO_PINS = [17, 27, 22, 10]
GPIO_DP = [25, 12, 16, 19]
GPIO_LED = [8, 20, 6, 5, 9, 7, 13, 11]

for i in GPIO_PINS:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
for i in GPIO_DP:
    GPIO.setup(i, GPIO.OUT)
    
for i in GPIO_LED:
    GPIO.setup(i, GPIO.OUT)

songs = [0, 1, 2, 3, 4]

e = {
    0: [False, False, False, True, False, False, False, True],
    1: [True, True, False, False, False, False, False, True],
    2: [False, True, True, False, False, False, True, True],
    3: [True, False, False, False, False, True, False, True],
    4: [False, True, True, False, False, False, False, True]
}

def writeLetter(digit, letter, scroll=False):
    for i in GPIO_DP:
        GPIO.output(i, False)
        
    GPIO.output(GPIO_DP[digit], True)

    for i in range(len(e[letter])):
        GPIO.output(GPIO_LED[i], e[letter][i])

    if(digit == 1 and scroll == False):
        GPIO.output(GPIO_LED[7], False)
    if(digit == 0 and scroll == True):
        GPIO.output(GPIO_LED[7], False)


timecodes = [0, 0, 0, 0, 0]
def Timer(id, cd=0.25):
    if(time() - timecodes[id] > cd):
        timecodes[id] = time()
        return True
    return False

scr = True

try:
    while True:    
        if(GPIO.input(GPIO_PINS[0]) == False):
            if(Timer(0)):
                songs = [songs[1], songs[2], songs[3], songs[4], songs[0]]
        if(GPIO.input(GPIO_PINS[1]) == False):
            if(Timer(1)):
                songs = [songs[4], songs[0], songs[1], songs[2], songs[3]]
        if(GPIO.input(GPIO_PINS[2]) == False):
            if(Timer(2)):
                songs = [songs[1], songs[0], songs[2], songs[3], songs[4]]
        if(GPIO.input(GPIO_PINS[3]) == False):
            if(Timer(3)):
                scr = not scr
                # timecodes[4] = time()

        # if(Timer(4, 5)):
        #     scr = not scr
        for i in range(4):
            writeLetter(i, songs[i+int(scr)], scr)
            sleep(0.001)   
except:
    for i in GPIO_DP:
        GPIO.output(i, False)
    GPIO.cleanup()
    print("Program Broke")