# MY CODE PART 1 ################################
import os
import time
import threading
def kill_prog():
    time.sleep(1)
    print('Killed')
    os._exit(1)
kill_thread = threading.Thread(target=kill_prog)
kill_thread.start()
# ###############################################

import sys
print(sys.argv)
# while True:
#     i = 0

# MY CODE PART 2 ################################
os._exit(1)
# ###############################################
