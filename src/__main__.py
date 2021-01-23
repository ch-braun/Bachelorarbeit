import argparse
import step01_data_collection
import step02_data_analysis
import step03_data_preprocessing
import step04_classification
import step05_evaluation
import step06_knowledge_representation


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean_scores', help='Remove ambiguously scored customers', action='store_true')
    parser.add_argument('--overwrite', help='Overwrite existing files', action='store_true')
    parser.add_argument('--skip_split', help='Skip splitting of files', action='store_true')
    parser.add_argument('--skip_stats', help='Skip creation of statistics', action='store_true')
    parser.add_argument('--skip_steps', help='Skip given steps (1 - 6)', nargs='+', metavar='N', type=int)

    return parser.parse_args()


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
