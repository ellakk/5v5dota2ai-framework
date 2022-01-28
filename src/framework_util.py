import ast
import importlib
import sys

from typing import Any


class BotClassError(Exception):
    pass


def load_class(path: str, filename: str, class_name: str) -> Any:
    """Loads a class, 'class_name' from 'path/filename'. The function
    returns the class as a value, not an instance of that class."""
    try:
        validate_bot_class(path + filename, class_name, 2)
        # It's intuitive to write path using slashes but import_module expects dots.
        dir_with_bots = path.replace('/', '.')
        filename_without_py = filename[:-3] if filename[-3:] == '.py' else filename
        module = importlib.import_module(dir_with_bots + filename_without_py)
        bot_cls = getattr(module, class_name)
        return bot_cls
    except ModuleNotFoundError as moduleError:
        raise BotClassError(moduleError)


def validate_bot_class(filename: str, class_name: str, n: int) -> None:
    """Validates that the bot class has exactly n arguments in its constructor."""
    try:
        with open(filename) as f:
            source = f.read()

        parsed_source = ast.parse(source)
        classes = [n for n in parsed_source.body if isinstance(n, ast.ClassDef)]
        bot_class = find_bot_class(classes, class_name)
        bot_class_functions = [f for f in bot_class.body if isinstance(f, ast.FunctionDef)]
        constructor = find_constructor(bot_class_functions)
        constructor_args = constructor.args.args

        if len(constructor_args) != n:
            names = f"({', '.join([arg.arg for arg in constructor_args])})"
            raise BotClassError(f"{class_name}'s constructor has the wrong number of args.\n"
                                f"Found {names} expected (self, world)")
    except FileNotFoundError:
        raise BotClassError(f"Couldn't open {filename}")


def find_bot_class(classes: list[ast.ClassDef], class_name: str) -> ast.ClassDef:
    for cls in classes:
        if cls.name == class_name:
            return cls

    raise BotClassError(f"The bot class file does not contain the specified class {class_name}")


def find_constructor(cls_functions: list[ast.FunctionDef]) -> ast.FunctionDef:
    for f in cls_functions:
        if f.name == '__init__':
            return f
    raise BotClassError(f"The bot class file does not contain an explicit constructor.")


def exit_with_error(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)
