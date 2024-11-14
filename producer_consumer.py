import threading
import time

# Variáveis globais para controle de identificadores de itens
item_counter = 1
item_counter_lock = threading.Lock()

class OperationCounter:
    def __init__(self):
        self.total_produced_operations = 0
        self.total_consumed_operations = 0

class Producer(threading.Thread):
    def __init__(self, buffer, max_operations, operation_lock, counter):
        super().__init__()
        self.buffer = buffer
        self.max_operations = max_operations
        self.operation_lock = operation_lock
        self.counter = counter

    def run(self):
        global item_counter
        while True:
            with self.operation_lock:
                if self.counter.total_produced_operations >= self.max_operations:
                    break
                self.counter.total_produced_operations += 1

            with item_counter_lock:
                item_id = item_counter
                item_counter += 1
            item = f"peça_{item_id}"
            self.buffer.add_item(item)
            print(f"Produtor {self.name} produziu: {item}")
            time.sleep(0.1)  # Simula o tempo de produção

class Consumer(threading.Thread):
    def __init__(self, buffer, max_operations, operation_lock, counter):
        super().__init__()
        self.buffer = buffer
        self.max_operations = max_operations
        self.operation_lock = operation_lock
        self.counter = counter

    def run(self):
        while True:
            with self.operation_lock:
                if self.counter.total_consumed_operations >= self.max_operations:
                    break
                self.counter.total_consumed_operations += 1

            item = self.buffer.remove_item()
            print(f"Consumidor {self.name} consumiu: {item}")
            time.sleep(0.1)  # Simula o tempo de consumo
