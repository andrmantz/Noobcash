import threading
import sys
import random
import requests
import pickle


class MiningThread:
    def __init__(self, mining_difficulty, address):
        self.block = None
        self.thread = None
        self.stop = threading.Event()
        self.mining_difficulty = mining_difficulty
        self.miner_lock = threading.Lock()
        self.address = address

    def run(self):
        with self.miner_lock:
            self.thread = threading.Thread(
                target=self.mine_block,
                args=[self.block, self.mining_difficulty, self.stop],
            )
            self.thread.daemon = True
            self.thread.start()
        return 0

    def mine_block(self, block, mining_difficulty, stop):

        if block.nonce:
            return
        while not stop.is_set():
            block.nonce = random.randint(0, sys.maxsize)
            if block.myHash().startswith("0" * mining_difficulty):
                # update
                block.hash = block.myHash()
                pickled_block = pickle.dumps(block)
                requests.post(f"http://{self.address}/mined", data=pickled_block)

    def running(self):
        return self.thread and self.thread.is_alive()

    def stop_mining(self):
        if self.running:
            self.stop.set()

    def clear_miner(self):
        with self.miner_lock:
            self.thread = None
            self.block = None
            self.stop.clear()

    def set_block(self, block):
        self.block = block
