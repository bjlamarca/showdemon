import threading
import time

class ThreadTracker:
    instance = None 
    threads_info = []

    
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
   
    def start_thread(cls, target, caller, *args):
        remove_thread = False
        thread_index = 0
        for index, thread_info in enumerate(cls.threads_info):
            if thread_info["target"] == target:
                if thread_info["thread"].is_alive():
                    print('Thread already exists and is running')
                    return True
                else:
                    print('Thread already exists but is not running')
                    remove_thread = True
                    thread_index = index

        if remove_thread:
            cls.threads_info.pop(thread_index)
        thread = threading.Thread(target=target, args=args)
        thread.daemon = True
        thread.start()
        thread_info = {'thread': thread, 'target': target, 'caller': caller, 'args': args}
        cls.threads_info.append(thread_info)

    def get_thread_info(cls, thread):
        for thread_info in cls.threads_info:
            if thread_info["thread"] == thread:
                
                return thread_info

    def get_all_thread_info(cls):
        for thread_info in cls.threads_info:
            print('thread', thread_info['thread'], '--', thread_info['thread'].is_alive())  
            
        return "Got it"

    def join_all(cls):
        for thread in cls.threads:
            thread.join()


