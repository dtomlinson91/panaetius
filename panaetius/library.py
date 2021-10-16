from __future__ import annotations

from typing import Any

from panaetius import Config


def set_config(
    config_inst: Config,
    key: str,
    default: Any = None,
    mask: bool = False,
    coerce: bool = False,
):
    config_var = key.lower().replace(".", "_")
    setattr(config_inst, config_var, config_inst.get_value(key, default, mask, coerce))
