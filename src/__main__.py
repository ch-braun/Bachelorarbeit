import argparse
import step01_data_collection
import step02_data_analysis
import step03_data_preprocessing
import step04_classification
import step05_evaluation
import step06_knowledge_representation


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean-scores', help='Remove ambiguously scored customers', action='store_true')
    parser.add_argument('--overwrite', help='Overwrite existing files', action='store_true')
    parser.add_argument('--skip-split', help='Skip splitting of files', action='store_true')
    parser.add_argument('--skip-stats', help='Skip creation of statistics', action='store_true')
    parser.add_argument('--skip-steps', help='Skip given steps (1 - 6)', nargs='+', metavar='N', type=int)
    parser.add_argument('--clear-flattened', help='Clear flattened directory', action='store_true')
    parser.add_argument('--skip-flattening', help='Skip flattening process', action='store_true')
    parser.add_argument('--skip-norm', help='Skip normalization process', action='store_true')
    parser.add_argument('--skip-independence-check', help='Skip normalization process', action='store_true')
    parser.add_argument('--crit-val', help='Critical value for corr. significance', nargs='?', metavar='a', type=float)
    parser.add_argument('--target-sampling-amount', help='Target sample amount', nargs='?', metavar='t', type=int)
    parser.add_argument('--epochs', help='Number of epochs to run', nargs='?', metavar='e', type=int)
    parser.add_argument('--use-normed', help='Use normalized data instead of independent', action='store_true')
    parser.add_argument('--neurons', help='Specify numbers of neurons', nargs='?', metavar='n', type=int)
    parser.add_argument('--skip-classification', help='Skip classification', action='store_true')
    parser.add_argument('--process-count', help='Specify the number of subprocesses', nargs='?', metavar='P', type=int)

    args = parser.parse_args()

    if args.process_count is None or args.process_count == 0:
        args.process_count = 1
    return args


def run_data_mining() -> None:
    args = parse_args()
    if args.skip_steps is None:
        args.skip_steps = list()

    if 1 not in args.skip_steps:
        step01_data_collection.do_step(args)

    if 2 not in args.skip_steps:
        step02_data_analysis.do_step(args)

    if 3 not in args.skip_steps:
        step03_data_preprocessing.do_step(args)

    if 4 not in args.skip_steps:
        step04_classification.do_step(args)

    if 5 not in args.skip_steps:
        step05_evaluation.do_step(args)

    if 6 not in args.skip_steps:
        step06_knowledge_representation.do_step(args)


if __name__ == '__main__':
    run_data_mining()
