# Tells the sim where to look for the data, and whether to enable debug.
from argparse import Namespace
import json

class Settings:

    # TODO - read from config to generate settings
    def __init__(self,
                 debug: bool = False,
                 demands_file: str = None,
                 bases_file: str = None,
                 cases_file: str = None,
                 travel_times_file: str = None,
                 num_ambulances: int = 5,
                 num_bases: int = 5,
                 args: Namespace = None
                 ):

        # TODO: Look for a settings file
        if args.settings:
            filename = "settings/" + args.settings + ".json"
            with open (filename, 'r') as jsonfile:
                s = json.load(jsonfile)

                filepath = s['filepath']
                demands_file = filepath + s['demands']
                bases_file = filepath + s['bases']
                travel_times_file = filepath + s['times']
                cases_file = filepath + s['cases']

                num_ambulances = s['num_ambs']
                num_bases = s['num_bases']


        # Assign the command line arguments into the parameter arguments
        if args.ambulances:
            num_ambulances = args.ambulances
        if args.bases:
            num_bases = args.bases

        # These are the parameters of the starship Enterprise
        self.data_filename = None
        self.debug = debug
        self.demands_file = demands_file
        self.bases_file = bases_file
        self.cases_file = cases_file
        self.travel_times_file = travel_times_file
        self.num_ambulances = num_ambulances
        self.num_bases = num_bases
