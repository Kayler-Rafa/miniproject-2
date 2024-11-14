from buffer import Buffer
from producer_consumer import Producer, Consumer, OperationCounter
import threading

def main():
    buffer_capacity = 10
    num_producers = 8
    num_consumers = 2
    timesteps = 100  # Total de operações de produção e consumo

    buffer = Buffer(buffer_capacity)
    counter = OperationCounter()  # Objeto compartilhado para contadores de operações
    operation_lock = threading.Lock()  # Lock para sincronizar contadores

    # Cria threads de produtores e consumidores com limite global de operações
    producers = [Producer(buffer, timesteps, operation_lock, counter) for _ in range(num_producers)]
    consumers = [Consumer(buffer, timesteps, operation_lock, counter) for _ in range(num_consumers)]

    # Inicia as threads
    for producer in producers:
        producer.start()
    for consumer in consumers:
        consumer.start()

    # Aguarda todas as threads finalizarem
    for producer in producers:
        producer.join()
    for consumer in consumers:
        consumer.join()

    # Relatório final
    print("\n=== RELATÓRIO FINAL ===")
    print(f"Total de itens produzidos: {counter.total_produced_operations}")
    print(f"Total de itens consumidos: {counter.total_consumed_operations}")
    print(f"Itens restantes no buffer: {len(buffer.buffer)}")

if __name__ == "__main__":
    main()
