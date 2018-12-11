class Counter:
    def __init__(self, name):
        self.name = name
        self.count = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def set(self, count):
        self.count = count
        
    def reset(self):
        self.set(0)

    def __str__(self):
        return 'Counter "{}": {}'.format(new.name, new.count)

if __name__ == "__main__":
    new = Counter("Deaths")
    print(new)
    new.increment()
    print(new)
    new.set(5)
    print(new)
    new.decrement()
    print(new)
    new.reset()
    print(new)