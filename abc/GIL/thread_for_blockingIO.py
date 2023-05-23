
def factorize(number):
    for i in range(1, number+1):
        if number % i == 0:
            yield i

from threading import Thread

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number
    
    def run(self):
        self.factors = list(factorize(self.number))


if __name__ == '__main__':
    import time
    numbers = [2139079, 1214759, 1516637, 1852285]
    start = time.time()
    for number in numbers:
        list(factorize(number))
    end = time.time()
    print(f'Serial execution took {end-start:.3f} seconds')


    # Use thread
    start = time.time()
    threads = []

    for number in numbers:
        thread = FactorizeThread(number)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    end = time.time()
    print(f'Use threading.Thread took {end-start:.3f} seconds')
