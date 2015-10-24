class EmailLabel:
    def __init__(self, label):
        self.label = label
        self.prior = 0
        self.densities = {}

    def __hash__(self):
        return hash(self.label)

    def get_prior(self):
        return self.prior

    def get_densities(self):
        return self.densities
