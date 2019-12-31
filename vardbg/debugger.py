from . import output
from .diff_processor import DiffProcessor
from .profiler import Profiler
from .replayer import Replayer
from .tracer import Tracer


class Debugger(DiffProcessor, Profiler, Replayer, Tracer):
    def __init__(self, relative_paths=True, json_output_path=None):
        # Whether to use relative paths over absolute ones in output
        self.use_relative_paths = relative_paths

        # Output writers
        writers = [output.ConsoleWriter()]
        if json_output_path is not None:
            writers.append(output.JsonWriter(json_output_path))
        self.out = output.OutputDelegate(*writers)

        # Initialize mixins
        super().__init__()

    def close(self):
        self.out.close()


def debug(func, *args, **kwargs):
    dbg = Debugger(*args, **kwargs)
    try:
        dbg.run(func)
    finally:
        dbg.close()


def replay(json_path, *args, **kwargs):
    dbg = Debugger(*args, **kwargs)
    try:
        dbg.replay(json_path)
    finally:
        dbg.close()