import time
from pyshell.loader import load_command
from pyshell.context import ShellContext


def run(args: list[str], context: ShellContext) -> None:
    """Measure execution time of a nested command in seconds."""
    if not args:
        context.print("timeit: missing command operand")
        return

    nested_cmd = args[0]
    nested_args = args[1:]
    cmd_str = " ".join(args)

    run_func = load_command(nested_cmd)

    t0 = time.perf_counter()
    run_func(nested_args, context)
    t1 = time.perf_counter()

    elapsed = t1 - t0
    context.print(f"`{cmd_str}` took {elapsed:.5f} seconds.")
