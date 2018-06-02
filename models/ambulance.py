from datetime import datetime

from geopy import Point


# Define the Ambulance model.

class Ambulance:

    def __init__(self,
                 id: int,
                 base: Point,
                 unit: str = "XXX-XXXX",
                 deployed: bool = False,
                 location: Point = None,
                 deployed_time: datetime = None,
                 end_time: datetime = None):
        self.id = id
        self.base = base
        self.unit = unit
        self.deployed = deployed
        self.location = location
        self.deployed_time = deployed_time
        self.end_time = end_time

    def __eq__(self, other):
        """
        Checks for equality
        :return: True if objects are equal; else False
        """

        if type(other) is Ambulance and self.id == other.id:
            return True

        return False

    # TODO default to ambulance base location?
    def finish(self, amb_location: Point):
        """
        Resets the ambulance.
        :return: None. This just changes state.
        """

        # Raise exception if ambulance is not deployed
        if not self.deployed:
            raise Exception("Ambulance {} not yet deployed, cannot finish".format(self.id))

        self.deployed = False
        self.location = amb_location
        self.deployed_time = None

    def deploy(self,
               location: Point,
               deployed_time: datetime,
               finish_time: datetime):
        """
        Deploys the ambulance by setting the deployed state, start times, end time, and location of the case.
        :param location
        :param deployed_time
        :param finish_time
        :return: Nothing. This function only changes state.
        """

        # Raise exception if ambulance is already deployed
        if self.deployed:
            raise Exception("Ambulance {} already deployed".format(self.id))

        self.deployed = True
        self.location = location
        self.deployed_time = deployed_time
        self.end_time = finish_time

    def __str__(self):
        return str([self.id, self.unit])