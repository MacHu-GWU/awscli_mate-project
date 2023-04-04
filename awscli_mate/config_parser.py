# -*- coding: utf-8 -*-

"""
``ConfigParser`` is a useful module for parsing and dumping ``.ini`` files,
but it lacks the ability to surgically modify specific key-value pairs
in config and credentials files without altering the accompanying comments.
Because ``ConfigParser`` does not preserve comments when dumping, it is
necessary to implement a custom tool for this purpose.

Reference:

- ConfigParser: https://docs.python.org/3/library/configparser.html
"""

import typing as T
import os
import dataclasses
import configparser
from pathlib import Path


@dataclasses.dataclass
class ConfigEditor:
    """
    :param file: Path to the config file
    :param _config: ``configparser.ConfigParser`` instance
    :param _data: ``dict`` of ``dict``s, where the first key is the section name
        and the second key is the key value pair in the section
    :param _lines: ``list`` of lines in the config file for in-memory editing
    """
    file: Path = dataclasses.field()
    _config: configparser.ConfigParser = dataclasses.field()
    _data: T.Dict[str, T.Dict[str, str]] = dataclasses.field()
    _lines: T.List[str] = dataclasses.field()

    @classmethod
    def from_file(cls, file: T.Union[str, Path]) -> "Config":
        file = Path(file)
        config = configparser.ConfigParser()
        config.read(str(file))
        data = dict()
        for section_name in config.sections():
            data[section_name] = dict(config[section_name].items())
        _lines = file.read_text().splitlines()
        return cls(
            file=Path(file),
            _config=config,
            _data=data,
            _lines=_lines,
        )

    def put(self, section: str, key: str, value: str):
        section_line = "[{}]".format(section)
        kv_line = f"{key} = {value}"

        flag_found_section = False
        flag_is_in_section = False
        flag_found_kv = False
        next_section_index = None

        for index, line in enumerate(self._lines):
            line = line.strip()
            # locate the section
                # # update the target_section_name section
                # new_lines.append(line)
                # for key, value in data:
                #     new_lines.append("{} = {}".format(key, value))
            # locate the section header first
            if line.startswith("[") and line.endswith("]"):
                if line == section_line:
                    flag_found_section = True
                    flag_is_in_section = True
                else:
                    if flag_found_section is True and flag_is_in_section is True:
                        next_section_index = index
                        break
                    flag_is_in_section = False
                continue

            if flag_is_in_section:
                if line.split("=")[0].strip() == key:
                    self._lines[index] = kv_line
                    flag_found_kv = True
                    break

        if flag_found_kv is False:
            if next_section_index is None:
                self._lines.append(kv_line)
            else:
                self._lines.insert(next_section_index, kv_line)

    def dump(self, file: T.Union[str, Path]):
        file = Path(file)
        file.write_text(os.linesep.join(self._lines))