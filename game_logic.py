class GameLogic:
    def __init__(self, total = 5):
        # ------- basic game setup -------
        self.total = total
        self.found = set()   # stores indexes of found differences
        self.mistakes = 0
        self.started = False

    def reset(self):
        # ------- restart everything -------
        self.found = set()
        self.mistakes = 0
        self.started = True

    def register_hit(self, i):
        # ------- correct click -------
        self.found.add(i)

    def register_miss(self):
        # ------- wrong click -------
        self.mistakes += 1

    def remaining(self):
        # ------- how many left -------
        return self.total - len(self.found)

    def is_won(self):
        # ------- all found? -------
        return len(self.found) == 5

    def is_lost(self):
        # ------- too many mistakes -------
        return self.mistakes >= 3