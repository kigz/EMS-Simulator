import argparse
import yaml
from IPython import embed

class UserArguments:
    """
    This class reads the arguments from the user from two sources of truth:
        1) the command line
        2) the config file

    Then it will self resolve discrepancies (?)

    """

    def __init__(self):
        """ Define the command line tool here. Use helper methods as needed. """

        cli_args = self._command_line_args()
        file_contents = yaml.load(open("./configurations/" + self.cli_args.configurations, 'r'))
        self.user_args = self._resolve_args(cli_args, file_contents)
        embed()

    def _resolve_args(self, cli, file):
        return 0

    def _command_line_args(self):

        parser = argparse.ArgumentParser(
            description="Load configurations, data, preprocess models. Run simulator on "
                        "ambulance dispatch. Decisions are made during the simulation, but "
                        "the events are output to a csv file for replay.")

        parser.add_argument('configurations',
                                 help="The simulator needs a configuration to begin the computaiton.",
                                 type=str,
                                 )

        parser.add_argument('--ambulances',
                                 help="Number of ambulances",
                                 type=int,
                                 required=False)

        parser.add_argument('--bases',
                                 help='Number of bases',
                                 type=int,
                                 required=False)

        parser.add_argument('--slices',
                                 help="Number of cases to simulate",
                                 type=int,
                                 required=False)

        parser.add_argument('--output-file',
                                 help="Output filename for simulator info",
                                 type=str,
                                 required=False)

        parser.add_argument('--debug',
                                 help="Whether the simulator should run in debug-mode.",
                                 type=bool,
                                 required=False,
                                 default=True)

        return parser.parse_args()
