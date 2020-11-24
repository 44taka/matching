import fire

import bin.omiai
import bin.pairs

class Pipeline(object):

    def __init__(self):
        self.omiai = bin.omiai.Omiai()
        self.pairs = bin.pairs.Pairs()

    def run(self):
        self.omiai.run()
        self.pairs.run()


if __name__ == "__main__":
    fire.Fire(Pipeline)
