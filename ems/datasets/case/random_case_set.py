from datetime import datetime

from ems.datasets.case.case_set import CaseSet
from ems.generators.duration.duration import DurationGenerator

from ems.generators.location.location import LocationGenerator
from ems.generators.event.event_generator import EventGenerator
from ems.generators.priority.priority import PriorityGenerator

from ems.models.cases.random_case import RandomCase


# Implementation of a case set that randomly generates cases while iterating
class RandomCaseSet(CaseSet):

    def __init__(self,
                 time: datetime,
                 case_time_generator: DurationGenerator,
                 case_location_generator: LocationGenerator,
                 case_priority_generator: PriorityGenerator,
                 event_generator: EventGenerator,
                 quantity: int = None):
        super().__init__(time)
        self.time = time
        self.case_time_generator = case_time_generator
        self.location_generator = case_location_generator
        self.priority_generator = case_priority_generator
        self.event_generator = event_generator
        self.quantity = quantity

    def iterator(self):
        k = 1

        while self.quantity is None or k <= self.quantity:
            # Compute time and location of next event via generators
            duration = self.case_time_generator.generate(timestamp=self.time)

            self.time = self.time + duration
            point = self.location_generator.generate(self.time)
            priority = self.priority_generator.generate(self.time)

            # Create case
            case = RandomCase(id=k,
                              date_recorded=self.time,
                              incident_location=point,
                              event_generator=self.event_generator,
                              priority=priority)

            k += 1

            yield case

    def __len__(self):
        return self.quantity
