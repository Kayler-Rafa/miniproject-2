import threading

class Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = []
        self.lock = threading.Lock()
        self.space_available = threading.Semaphore(capacity)
        self.items_available = threading.Semaphore(0)

    def add_item(self, item):
        self.space_available.acquire()  # Espera por espaço disponível
        with self.lock:
            self.buffer.append(item)
            print(f"Item produzido. Buffer: {len(self.buffer)}/{self.capacity}")
        self.items_available.release()  # Libera um item disponível

    def remove_item(self):
        self.items_available.acquire()  # Espera por um item disponível
        with self.lock:
            item = self.buffer.pop(0)
            print(f"Item consumido. Buffer: {len(self.buffer)}/{self.capacity}")
        self.space_available.release()  # Libera espaço no buffer
        return item
