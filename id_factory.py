class IdFactory:
    def __init__(self):
        self.cell_id_counter = 0
        self.mover_id_counter = 0

    def cell_id(self) -> int:
        self.cell_id_counter += 1
        return self.cell_id_counter

    def mover_id(self) -> int:
        self.mover_id_counter += 1
        return self.mover_id_counter
id_factory = IdFactory()