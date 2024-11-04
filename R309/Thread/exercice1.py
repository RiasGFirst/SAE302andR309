import threading
import time

def print_message(j: int) -> None:
    """
    Print the message "Je suis la thread {i}" 5 times
    :param i:
    :return:
    """
    if not isinstance(j, int):
        raise ValueError("j must be an integer")
    for i in range(5):
        print(f"Je suis la thread {j}")
        time.sleep(1)


if __name__ == '__main__':
    # Create threads
    t1 = threading.Thread(target=print_message, args=(1,))
    t2 = threading.Thread(target=print_message, args=(2,))
    # Start threads
    t1.start()
    t2.start()
    # Wait for threads to finish
    t1.join()
    t2.join()
