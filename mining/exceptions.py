class MiningActionThrottledError(Exception):

    def __init__(self, next_mining_in_seconds: int):
        super().__init__(f'Next mining in {next_mining_in_seconds} seconds')
        self.next_mining_in_seconds = next_mining_in_seconds
