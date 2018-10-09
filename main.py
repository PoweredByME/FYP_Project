'''
    This is the main entry point of the entire code.
'''

from queue import Queue;
from worker import Worker;
import time;

def main():
    input_q = Queue(100);
    output_q = Queue(100);
    threadPool = [Worker(input_q, output_q, str(i)) for i in range(10)];
    try:
        # make a thread pool which contains all the thread which are to be executed.
        # start all threads in the pool.
        for _thread in threadPool:
            _thread.start();

        for i in range(1000000):
            input_q.put(i);

    finally:
        # execute the clean up code.
        for _thread in threadPool:
            _thread.join();




# Call main function if this script is the main script.
if __name__ == "__main__":
    main();