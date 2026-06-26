# SPDX-License-Identifier: MIT

from pathlib import Path

import pytest

from scripts.link_freecad_workbench import (
    WORKBENCH_DIR_NAME,
    default_mod_dir,
    default_workbench_source,
    link_workbench,
)


def test_default_mod_dir_uses_freecad_user_mod_path():
    assert default_mod_dir(Path("/home/dev")) == Path("/home/dev/.local/share/FreeCAD/Mod")


def test_default_workbench_source_uses_repo_root_controlforgecad():
    assert default_workbench_source(Path("/repo")) == Path("/repo/ControlForgeCAD")


def test_link_workbench_creates_mod_directory_symlink(tmp_path):
    source = tmp_path / WORKBENCH_DIR_NAME
    mod_dir = tmp_path / "FreeCAD" / "Mod"
    source.mkdir()

    target = link_workbench(source, mod_dir)

    assert target == mod_dir / WORKBENCH_DIR_NAME
    assert target.is_symlink()
    assert target.resolve() == source.resolve()


def test_link_workbench_is_idempotent_for_existing_matching_symlink(tmp_path):
    source = tmp_path / WORKBENCH_DIR_NAME
    mod_dir = tmp_path / "Mod"
    source.mkdir()

    first_target = link_workbench(source, mod_dir)
    second_target = link_workbench(source, mod_dir)

    assert second_target == first_target


def test_link_workbench_rejects_existing_non_symlink(tmp_path):
    source = tmp_path / WORKBENCH_DIR_NAME
    mod_dir = tmp_path / "Mod"
    source.mkdir()
    mod_dir.mkdir()
    (mod_dir / WORKBENCH_DIR_NAME).mkdir()

    with pytest.raises(FileExistsError, match="not a symlink"):
        link_workbench(source, mod_dir)
