'''
import threading
import time

class BarberShop:
    def __init__(self, num_chairs):
        self.num_chairs = num_chairs
        self.barber_sleeping = threading.Event()
        self.barber_sleeping.set()
        self.chairs = threading.Semaphore(num_chairs)

    def enter_barbershop(self, customer_id):
        if not self.barber_sleeping.is_set():
            if self.chairs.acquire(blocking=False):
                self.barber_sleeping.wait()
                self.chairs.release()
                self.get_haircut(customer_id)
            else:
                print(f"Customer {customer_id} left the barbershop")
        else:
            self.chairs.acquire()
            self.barber_sleeping.clear()
            self.chairs.release()
            self.get_haircut(customer_id)

    def get_haircut(self, customer_id):
        print(f"Customer {customer_id} is getting a haircut")
        # Simulating the haircut
        time.sleep(2)
        print(f"Customer {customer_id} has finished the haircut")
        self.leave_barbershop()

    def leave_barbershop(self):
        print("Customer is leaving the barbershop")
        self.barber_sleeping.set()


def main():
    num_chairs = 3
    shop = BarberShop(num_chairs)

    customers = [threading.Thread(target=shop.enter_barbershop, args=(i,)) for i in range(10)]
    barber = threading.Thread(target=shop.leave_barbershop)

    barber.start()
    for customer in customers:
        customer.start()

    for customer in customers:
        customer.join()
    barber.join()


if __name__ == "__main__":
    main()
'''
import threading
import time

# Класс для события "клиент пришел"
class ClientArrivedEvent(threading.Event):
    pass

# Класс для события "клиент обслужен"
class ClientDoneEvent(threading.Event):
    pass

class BarberShop:
    def __init__(self, num_chairs):
        self.num_chairs = num_chairs
        self.chairs = [threading.Lock() for _ in range(num_chairs)]
        self.barber_chair = threading.Lock()
        self.clients_arrived = ClientArrivedEvent()
        self.client_done = ClientDoneEvent()
        self.customers = 0

    def barber(self):
        while True:
            print("Barber is sleeping")
            self.clients_arrived.wait() # ожидаем пока клиент придет
            self.barber_chair.acquire() # занимаем кресло парикмахера
            self.clients_arrived.clear() # сбрасываем событие "клиент пришел"
            print("Barber is cutting hair")
            self.cut_hair() # стригем волосы
            self.barber_chair.release() # освобождаем кресло парикмахера
            self.client_done.set() # устанавливаем событие "клиент обслужен"

    def customer(self, client_num):
        if client_num >= self.num_chairs:
            print(f"Client {client_num} couldn't take chair, leaving...")
            return
        with self.chairs[client_num]:
            # если не удалось занять кресло парикмахера
            if not self.barber_chair.acquire(blocking=False):
                print(f"Client {client_num} couldn't take barber's chair, leaving...")
                return
            print(f"Client {client_num} is getting hair cut")
            self.customers += 1
            if self.customers == 1:
                self.clients_arrived.set() # устанавливаем событие "клиент пришел"
            self.barber_chair.release() # освобождаем кресло парикмахера

            self.client_done.wait() # ожидаем пока клиент будет обслужен
            self.client_done.clear() # сбрасываем событие "клиент обслужен"
            print(f"Client {client_num} is leaving after getting hair cut")
            self.customers -= 1

    def cut_hair(self):
        # симуляция стрижки
        time.sleep(2)

# Создаем парикмахерскую с 3 стульями для клиентов
barber_shop = BarberShop(3)

# Создаем поток для парикмахера
barber_thread = threading.Thread(target=barber_shop.barber)
# Запускаем поток парикмахера
barber_thread.start()

# Создаем 5 потоков для клиентов
customer_threads = []
for i in range(5):
    customer_threads.append(threading.Thread(target=barber_shop.customer, args=(i,)))

# Запускаем потоки клиентов
for thread in customer_threads:
    thread.start()

# Ожидаем завершения потоков клиентов
for thread in customer_threads:
    thread.join()

# Завершаем поток парикмахера
barber_thread.join()