import Queue

if __name__ == '__main__':
    queue = Queue.Queue(5)

    queue.put_nowait(1)
    queue.put_nowait(2)
    queue.put_nowait(3)
    queue.put_nowait(4)
    queue.put_nowait(5)

    try:
        queue.put_nowait(6)
    except Queue.Full:
        print 'queue is full!'

    print 'queue size:', queue.qsize()

    for n in queue.queue:
        print "Queue entry: " + str(n)
