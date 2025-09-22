import random


class Apple:
    def __init__(self, position: tuple, remaining_apples: int):
        self.position = position
        self.remaining_apples = remaining_apples

    def respawn(self, rows: int, cols: int, occupied: set):
        while True:
            new_pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
            if new_pos not in occupied or self.remaining_apples == 0:
                self.position = new_pos
                self.remaining_apples -= 1
                break
