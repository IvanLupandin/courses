class Board:
    def __int__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self, size=6, hid=False):
        self.hid = hid
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        self.field = [["O"] * size for _ in range(size)]
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " | "
        if self.hid:
            res = res.replace("■", "О")
        return res

b = Board()
print(b)