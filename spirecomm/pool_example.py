from time import sleep
from multiprocessing import Process
import multiprocessing


def func(x, called_from):
    print("start %s from %s" % (x, called_from))
    sleep(x)
    print("end %s from %s" % (x, called_from))
    return


if __name__ == '__main__':

    Process(target=func, args=(0.5, '1')).start()
    Process(target=func, args=(0.5, '2')).start()
