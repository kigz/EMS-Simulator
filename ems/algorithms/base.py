from ems.datasets.location import LocationSet


class AmbulanceBaseSelector:

    # TODO -- More info
    def select(self, num_ambulances):
        raise NotImplementedError()


class RoundRobinBaseSelector(AmbulanceBaseSelector):
    """ Assigned ambulances to bases in round robin order.  """

    def __init__(self,
                 base_set: LocationSet):
        self.base_set = base_set

    def select(self, num_ambulances):
        bases = []

        for index in range(num_ambulances):
            base_index = index % len(self.base_set)
            bases.append(self.base_set.locations[base_index])

        return bases
