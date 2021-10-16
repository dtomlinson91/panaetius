from __future__ import annotations
import ast
from typing import Any

from panaetius import Config


def set_config(
    config_inst: Config,
    key: str,
    default: str | None = None,
    mask: bool = False,
    coerce: bool = False,
):  # sourcery skip: remove-redundant-pass
    config_var = key.lower().replace(".", "_")
    if not coerce:
        setattr(config_inst, config_var, config_inst.get_value(key, default, mask))
    elif type(config_inst.get_value(key, default, mask)) is not coerce:  # noqa
        var = ast.literal_eval(config_inst.get_value(key, default, mask))
        if isinstance(var, (list, dict)):
            setattr(config_inst, config_var, var)
        else:
            pass
            # TODO: raise error to say type of coersion isn't valid!
