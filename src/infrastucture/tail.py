import sys
import os
import time
from threading import Thread


class Tail(object):
    """
    Python-Tail - Unix tail follow implementation in Python.

    python-tail can be used to monitor changes to a file.

    Example:
        import tail

        # Create a tail instance
        t = tail.Tail('file-to-be-followed')

        # Register a callback function to be called when a new line is found in the followed file.
        # If no callback function is registerd, new lines would be printed to standard out.
        t.register_callback(callback_function)

        # Follow the file with 5 seconds as sleep time between iterations.
        # If sleep time is not provided 1 second is used as the default time.
        t.follow(s=5)
    """

    ''' Represents a tail command. '''

    def __init__(self, tailed_file):
        ''' Initiate a Tail instance.
            Check for file validity, assigns callback function to standard out.

            Arguments:
                tailed_file - File to be followed. '''
        self.__check_file_validity(tailed_file)
        self.tailed_file = tailed_file
        self.callback = sys.stdout.write
        self.is_running = True
        self.try_count = 0

        try:
            self.file_ = open(self.tailed_file, "r")
            self.size = os.path.getsize(self.tailed_file)

            # Go to the end of file
            self.file_.seek(0, 2)
        except:
            raise

    def reload_tailed_file(self):
        """ Reload tailed file when it be empty be `echo "" > tailed file`, or
            segmentated by logrotate.
        """
        try:
            self.file_ = open(self.tailed_file, "r")
            self.size = os.path.getsize(self.tailed_file)

            # Go to the head of file
            self.file_.seek(0, 1)

            return True
        except:
            return False

    def __follow(self, s=0.01):
        """ Do a tail follow. If a callback function is registered it is called with every new line.
        Else printed to standard out.

        Arguments:
            s - Number of seconds to wait between each iteration; Defaults to 1. """
        while self.is_running:
            _size = os.path.getsize(self.tailed_file)
            if _size < self.size:
                while self.try_count < 10:
                    if not self.reload_tailed_file():
                        self.try_count += 1
                    else:
                        self.try_count = 0
                        self.size = os.path.getsize(self.tailed_file)
                        break
                    time.sleep(0.1)

                if self.try_count == 10:
                    raise Exception("Open %s failed after try 10 times" % self.tailed_file)
            else:
                self.size = _size

            curr_position = self.file_.tell()
            line = self.file_.readline()
            if not line:
                self.file_.seek(curr_position)
            elif not line.endswith("\n"):
                self.file_.seed(curr_position)
            else:
                self.callback(line)
            time.sleep(s)

    def register_callback(self, func):
        """ Overrides default callback function to provided function. """
        self.callback = func

    def __check_file_validity(self, file_):
        """ Check whether the a given file exists, readable and is a file """
        if not os.access(file_, os.F_OK):
            raise TailError("File '%s' does not exist" % (file_))
        if not os.access(file_, os.R_OK):
            raise TailError("File '%s' not readable" % (file_))
        if os.path.isdir(file_):
            raise TailError("File '%s' is a directory" % (file_))

    def start(self):
        self.__theard = Thread(target=self.__follow)
        self.__theard.setDaemon(True)
        self.__theard.start()

    def stop(self):
        if self.__theard:
            self.is_running = False


class TailError(Exception):
    """ Custom error type.
    """

    def __init__(self, msg):
        """ Init.
        """
        self.message = msg

    def __str__(self):
        """ str.
        """
        return self.message


if __name__ == '__main__':
    t = Tail("/Users/mudi/Coding/workspace-python/nova/test/logs/wireless-payment/log_info.log")
    t.register_callback(lambda x: print("---" + x))
    t.start()
    time.sleep(20)
    t.stop()
