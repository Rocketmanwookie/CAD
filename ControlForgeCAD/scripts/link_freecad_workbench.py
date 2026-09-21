#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Link a development checkout into FreeCAD's user Mod directory."""

from __future__ import annotations

import argparse
from pathlib import Path


WORKBENCH_DIR_NAME = "ControlForgeCAD"


def default_mod_dir(home: Path) -> Path:
    return home / ".local" / "share" / "FreeCAD" / "Mod"


def default_workbench_source(repository_root: Path) -> Path:
    return repository_root / WORKBENCH_DIR_NAME


def link_workbench(source: Path, mod_dir: Path) -> Path:
    source = source.expanduser().resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"Workbench source does not exist: {source}")
    target = mod_dir.expanduser() / WORKBENCH_DIR_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.is_symlink() and target.resolve() == source:
            return target
        if target.is_symlink():
            raise FileExistsError(f"Existing workbench symlink points elsewhere: {target}")
        raise FileExistsError(f"Existing workbench target is not a symlink: {target}")
    target.symlink_to(source, target_is_directory=True)
    return target


def main() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=default_workbench_source(repository_root))
    parser.add_argument("--mod-dir", type=Path, default=default_mod_dir(Path.home()))
    args = parser.parse_args()
    target = link_workbench(args.source, args.mod_dir)
    print(f"Linked {target} -> {target.resolve()}")


if __name__ == "__main__":
    main()
