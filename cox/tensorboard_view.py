from .readers import CollectionReader
from .utils import has_tensorboard
from argparse import ArgumentParser
import subprocess
import os
from os.path import join
import re
#http://localhost:8001/source/examples/2.html#walkthrough-2-using-cox-with-tensorboardx

def main():
    '''
    This function is meant to be run via command line (see
    `Walkthrough 2 <https://cox.readthedocs.io/en/latest/examples/2.html>`_ for more information.
    '''
    parser = ArgumentParser(description='Helper script for starting interpretable tensorboard sessions.')
    parser.add_argument('--logdir', type=str, required=True, help="logdir (Same as tensorboard)")
    parser.add_argument('--port', type=int, required=False, default=6006, help="Port (passed on to tensorboard")
    parser.add_argument('--metadata-table', type=str, default="metadata", help="Name of the metadata table")
    parser.add_argument('--format-str', type=str, required=True,  \
                    help="How to format the job name prefix (the suffix is always the uid)")
    parser.add_argument('--filter-param', action='append', nargs=2, help='Format: {parameter} {required value regex}')
    args = parser.parse_args()

    reader = CollectionReader(args.logdir)
    metadata_df = reader.df(args.metadata_table)
    all_params = list(metadata_df.keys())

    # Find all of the valid experiments, i.e. folders with a tensorboard/ directory inside of them
    subdirs = filter(lambda x: has_tensorboard(join(args.logdir, x)), os.listdir(args.logdir))

    filters = {}
    if args.filter_param is not None:
        filters = dict(args.filter_param)

    tensorboard_arg_str = ""
    for exp_id in subdirs:
        params_to_fill = {}
        try:
            for p in all_params:
                param_value = metadata_df[metadata_df['exp_id'] == exp_id][p][0]
                if p in filters and re.match(filters[p], str(param_value)) is None:
                    raise ValueError("Filtered out---this exception will be caught.")
                if type(param_value) == list:
                    param_value = '.'.join([str(x) for x in param_value])

                params_to_fill[p] = param_value
            name_str = args.format_str.format(**params_to_fill) + "---" + exp_id
            tensorboard_arg_str += f"{name_str}:{join(args.logdir, exp_id)},"
        except IndexError as ie:
            print("Warning: Skipping experiment %s" % (exp_id,))
        except ValueError as ve:
            pass
    
    cmd_to_run = f"tensorboard --logdir {tensorboard_arg_str} --port {args.port}"
    print(f"Running '{cmd_to_run}'")
    os.system(cmd_to_run)

if __name__ == "__main__":
    main()
