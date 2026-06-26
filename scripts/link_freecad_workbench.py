#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Link the ControlForgeCAD workbench into FreeCAD's user Mod directory."""

from __future__ import annotations

import argparse
from pathlib import Path


WORKBENCH_DIR_NAME = "ControlForgeCAD"


def default_mod_dir(home: Path | None = None) -> Path:
    base_home = home if home is not None else Path.home()
    return base_home / ".local" / "share" / "FreeCAD" / "Mod"


def default_workbench_source(repo_root: Path | None = None) -> Path:
    root = repo_root if repo_root is not None else Path(__file__).resolve().parents[1]
    return root / WORKBENCH_DIR_NAME


def link_workbench(source: Path, mod_dir: Path, link_name: str = WORKBENCH_DIR_NAME) -> Path:
    source_path = source.resolve()
    if not source_path.is_dir():
        raise FileNotFoundError(f"Workbench source does not exist: {source_path}")

    mod_dir.mkdir(parents=True, exist_ok=True)
    target = mod_dir / link_name

    if target.is_symlink():
        current = target.resolve()
        if current == source_path:
            return target
        raise FileExistsError(f"{target} already links to {current}")

    if target.exists():
        raise FileExistsError(f"{target} already exists and is not a symlink")

    target.symlink_to(source_path, target_is_directory=True)
    return target


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a FreeCAD user Mod symlink for the ControlForgeCAD workbench."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=default_workbench_source(),
        help="Path to the ControlForgeCAD workbench directory.",
    )
    parser.add_argument(
        "--mod-dir",
        type=Path,
        default=default_mod_dir(),
        help="Path to FreeCAD's user Mod directory.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    target = link_workbench(args.source, args.mod_dir)
    print(f"Linked {target} -> {args.source.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
