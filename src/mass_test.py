import os
# normed neurons = 446
# independent neurons = 61

args = ['--skip-steps 1 2 3 5 6 --epochs 100 --neurons 61',
        '--skip-steps 1 2 3 5 6 --epochs 100 --neurons 61 --target-sampling-amount 1000',
        '--skip-steps 1 2 3 5 6 --epochs 100 --neurons 61 --target-sampling-amount 5000',
        '--skip-steps 1 2 3 5 6 --epochs 100 --neurons 61 --target-sampling-amount 10000',
        '--skip-steps 1 2 3 5 6 --epochs 100 --neurons 446 --use-normed',
        '--skip-steps 1 2 3 5 6 --epochs 100 --neurons 446 --use-normed --target-sampling-amount 1000',
        '--skip-steps 1 2 3 5 6 --epochs 100 --neurons 446 --use-normed --target-sampling-amount 5000',
        '--skip-steps 1 2 3 5 6 --epochs 100 --neurons 446 --use-normed --target-sampling-amount 10000',
        ]

for arg in args:
    command = 'python3 src/__main__.py ' + arg
    print(command)
    os.system(command)
