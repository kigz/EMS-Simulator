from typing import List

import numpy as np

from ems.datasets.location.kd_tree_location_set import KDTreeLocationSet
from ems.datasets.travel_times.travel_times import TravelTimes
from ems.utils import parse_headered_csv


class FilteredBaseSet(KDTreeLocationSet):

    def __init__(self,
                 count: int,
                 required_travel_time: int,
                 travel_times: TravelTimes,
                 filename: str = None,
                 latitudes: List[float] = None,
                 longitudes: List[float] = None):
        self.filename = filename
        self.count = count
        self.required_travel_time = required_travel_time
        self.travel_times = travel_times

        if filename is not None:
            latitudes, longitudes = self.read_bases(filename)

        latitudes, longitudes = self.kmeans_filter(latitudes, longitudes)
        super().__init__(latitudes, longitudes)

    def read_bases(self, filename):
        # Read bases from a headered CSV into a pandas dataframe
        base_headers = ["latitude", "longitude"]
        bases_df = parse_headered_csv(filename, base_headers)

        # Generate list of models from dataframe
        latitudes = []
        longitudes = []
        for index, row in bases_df.iterrows():
            latitudes.append(row["latitude"])
            longitudes.append(row["longitude"])

        return latitudes, longitudes

    def kmeans_filter(self, latitudes, longitudes):

        self.latitudes = latitudes
        self.longitudes = longitudes

        # indices = [i for i in range(len(latitudes)- 1)]
        # from multiprocessing import Pool
        # with Pool(8) as p:
        #     bases_and_coverages = p.map(self.kmeans_filter_i, indices)
        #
        #
        #
        # from IPython import embed; embed()
        # return None




    # def kmeans_filter_i(self, i):

        i = 0

        np_travel_times = np.array(self.travel_times.times)
        chosen_latitudes = []
        chosen_longitudes = []
        demands_covered = 0

        first_time = True

        for _ in range(self.count):

            if not first_time: i = 0

            # Make a True/False table of the travel_times and then count how many covered.
            covered = [[t < self.required_travel_time for t in row] for row in np_travel_times]
            count_covered = [(index, covered[index].count(True)) for index in range(len(covered))]
            d = [('index', int), ('covered', int)]
            count_covered = np.array(count_covered, d)

            # Sort the table by row and grab the last element (the base with the most coverage)
            (best_base, count) = np.sort(count_covered, order='covered', kind='mergesort')[-1 - i]
            first_time = False
            # print(best_base, count)
            chosen_latitudes.append(self.latitudes[best_base])
            chosen_longitudes.append(self.longitudes[best_base])
            demands_covered += count
            demand_coverage = covered[best_base]

            # Delete the covered columns
            delete_cols = [d for d in range(len(demand_coverage)) if demand_coverage[d]]
            np_travel_times = np.delete(np_travel_times, delete_cols, axis=1)

        if demands_covered >= 99: print(demands_covered)
        # return chosen_latitudes, chosen_longitudes, demands_covered
        return chosen_latitudes, chosen_longitudes
