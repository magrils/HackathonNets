import getch
import signal
def handler(signal_num,frame):
    raise Exception()

def loop():
    print("start typing")
    while True:
        try:
            x = getch.getch()
            if x=='q':
                break
            print("you typed in\ " + x)
        except:
            break
    print("end typing")

def Main():
    signal.signal(signal.SIGALRM,handler)
    signal.alarm(10)
    try:
        loop()
    except:
        print("my error")

    signal.alarm(0)



if __name__ == '__main__':
    Main()