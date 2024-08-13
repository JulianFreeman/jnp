# coding: utf8
import os
from pathlib import Path


def path_not_exist(path: str | Path) -> bool:
    """
    判断目标路径是否存在
    如果参数为空或者 None，亦认为不存在

    :param path: 目标路径
    :return:
    """
    if isinstance(path, str):
        return len(path) == 0 or not Path(path).exists()
    elif isinstance(path, Path):
        return not path.exists()
    else:
        return True


def path_exists(path: str | Path) -> bool:
    """
    对 path_not_exist 的相反包装

    :param path: 目标路径
    :return:
    """
    return not path_not_exist(path)


def get_log_dir(plat: str) -> str | None:
    match plat:
        case "win32":
            log_dir = os.path.expandvars("%appdata%")
        case "darwin":
            log_dir = os.path.expanduser("~") + "/Library/Application Support"
        case _:
            return None
    if path_exists(log_dir):
        return log_dir
    else:
        return None
