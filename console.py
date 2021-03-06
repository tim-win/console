"""Drop some shit to terminal."""

from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

from Queue import Queue
from Queue import Empty

from threading import Thread

import time


def enqueue(pipe, queue):
    """Takes a pipe and a queue, and unloads.
    
    Parameters
    ----------
    pipe : subprocess.Popen.stdout.
        A file-like object.
    
    queue : Queue.Queue
        A FIFO Queue.
    """
    for line in iter(pipe.readline, b''):
        queue.put(line)
    pipe.close()


def read_queue(queue):
    """Return everything from the queue in a dandy string.
    Logic is to handle the terminal case of queue being empty.

    Parameters
    ----------
    queue : Queue.Queue

    Returns
    -------
    str : queue contents

    SideEffects
    -----------
    Depopulates the queue provided.
    """
    output = ''
    try:
        # Non blocking queue population
        while True:
            # Raises Queue.Empty on empty queue
            output += queue.get_nowait()

    # Catch and Return
    except Empty:
        return output


def interactive_console(cmd_list, inputs=None):
    """Interactive console.

    Parameters
    ----------
    cmd : list : str
        Command list. no pipes, please. Command list means docker cmd style:
            ['echo', 'ok']
        If you pass it ['echo ok'] you'll have a bad time.

    inputs : list : str
        list of string responses to send. If empty, ignored

    Returns
    -------
    bool : True if successful
    """
    process = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout_queue = Queue()
    stdout_thread = Thread(target=enqueue, args=(process.stdout, stdout_queue))
    stdout_thread.daemon= True
    stdout_thread.start()

    if inputs is None:
        inputs = []

    for str_input in inputs:
        process.stdin.write(str_input + '\n')

    while process.poll() is None:
        output = read_queue(stdout_queue)
        if output:
            print output
        time.sleep(1)

    output = read_queue(stdout_queue)
    if output:
        print output

    return True
