import threading
import time

def countdown(name: str, n: int) -> None:
    """
    countdown that print the name and the number n until n is 0
    :param name:
    :param n:
    :return:
    """
    if not isinstance(name, str):
        raise ValueError('name must be a string')
    if not isinstance(n, int):
        raise ValueError('n must be an integer')
    if n < 0:
        raise ValueError('n must be a positive integer')
    while n > 0:
        print(name, n)
        n -= 1
        time.sleep(1)


if __name__ == '__main__':
    # Create two threads as follows
    t1 = threading.Thread(target=countdown, args=('Thread 1', 5))
    t2 = threading.Thread(target=countdown, args=('Thread 2', 3))
    # Start new Threads
    t1.start()
    t2.start()
    # Wait for all threads to complete
    t1.join()
    t2.join()