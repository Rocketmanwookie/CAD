# SPDX-License-Identifier: MIT
"""Minimal Qt review dialog for staged project imports."""

from __future__ import annotations

from pathlib import Path

from controls_wb.gui.io_signal import _qt_widgets
from controls_wb.gui.project_intake import existing_project_object
from controls_wb.import_review import StagedProjectImport, stage_project_import


def choose_staged_project_import(document: object, parent=None) -> tuple[StagedProjectImport, set[str]] | None:
    """Choose a supported file and return only user-approved staged fields.

    This function never writes to ``document``.  The command boundary applies
    its returned decision inside the document transaction.
    """

    QtWidgets = _qt_widgets()
    source_path, _selected_filter = QtWidgets.QFileDialog.getOpenFileName(
        parent,
        "Import and Review Controls Project",
        "",
        "Supported project files (*.xml *.ceproject *.yaml *.yml *.uml *.puml *.plantuml *.txt);;All files (*)",
    )
    if not source_path:
        return None
    try:
        source_text = Path(source_path).read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"Unable to read import file: {exc}") from exc
    staged = stage_project_import(source_text, source_path, existing_project_object(document))
    if not staged.candidates:
        raise RuntimeError("The import has no changed supported fields to review.")

    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Review Imported Project Data")
    layout = QtWidgets.QVBoxLayout(dialog)
    layout.addWidget(QtWidgets.QLabel("Select each proposed field to approve. Unchecked fields are not imported."))
    if staged.warnings:
        layout.addWidget(QtWidgets.QLabel("Import warnings:\n" + "\n".join(staged.warnings)))
    approvals = {}
    for candidate in staged.candidates:
        checkbox = QtWidgets.QCheckBox(
            f"[{candidate.category}] {candidate.key}: {candidate.current_value or '<empty>'} → {candidate.proposed_value or '<empty>'}"
        )
        approvals[candidate.key] = checkbox
        layout.addWidget(checkbox)
    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    execute = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if execute() != QtWidgets.QDialog.Accepted:
        return None
    return staged, {key for key, checkbox in approvals.items() if checkbox.isChecked()}
