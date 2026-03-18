import threading

class __SingletonWrapper:
    def __init__(self, cls):
        self.__wrapped__ = cls
        self._instance = None
        self._lock = threading.Lock()

    def __call__(self, *args, **kwargs):
        with self._lock:
            if self._instance is None:   
                self._instance = self.__wrapped__(*args, **kwargs)
        
        return self._instance

def singleton(cls):
    return __SingletonWrapper(cls)