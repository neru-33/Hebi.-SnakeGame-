import random


class Apple:
    def __init__(self, position: tuple):
        self.position = position

    def respawn(self, rows: int, cols: int, occupied: set):
        while True:
            new_pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
            if new_pos not in occupied:
                self.position = new_pos
                break
