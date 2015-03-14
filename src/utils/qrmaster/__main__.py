from sys import argv
from generate import generate

argn = len(argv)
get_arg = lambda n, d=None: argv[n] if argn>=n+1 else d

generate(
    eval(
        get_arg(1)
    ),
    get_arg(2),
    get_arg(3),
    get_arg(4),
    get_arg(5)
)
