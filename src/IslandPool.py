from Island import Island


"""
This defines an island pool which contains many islands.
Each island runs genetic evolution separateley.
"""
class IslandPool:
    def __init__(self, num_islands, migration_frequency) -> None:
        self.islands: list[Island] = [Island()] * num_islands
        self.num_islands = num_islands

        self.migration_frequency = migration_frequency

    def add_island() -> None:
        pass
