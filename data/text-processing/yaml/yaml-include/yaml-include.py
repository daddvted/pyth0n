import os
import json
from typing import Any, IO

import yaml


class IncludeLoader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)


def construct_include(loader: IncludeLoader, node: yaml.Node) -> Any:

    filename = os.path.abspath(os.path.join(loader._root, loader.construct_scalar(node)))
    # print(filename)
    extension = os.path.splitext(filename)[1].lstrip('.')

    with open(filename, 'r') as f:
        if extension in ('yaml', 'yml'):
            return yaml.load(f, IncludeLoader)
        elif extension in ('json', ):
            return json.load(f)
        else:
            return ''.join(f.readlines())


yaml.add_constructor('!include', construct_include, IncludeLoader)


if __name__ == '__main__':
    with open('stack.yaml', 'r') as f:
        data = yaml.load(f, IncludeLoader)
    #print(data)
    print(yaml.dump(data))
