# SPDX-License-Identifier: MIT
"""Minimal Qt review dialog for staged project imports."""

from __future__ import annotations

from pathlib import Path

from controls_wb.gui.io_signal import _qt_widgets
from controls_wb.gui.project_intake import existing_project_object
from controls_wb.io_list import explicit_io_signals_from_project
from controls_wb.import_review import (
    StagedIOImport,
    StagedProjectImport,
    stage_ceproject_io_import,
    stage_project_import,
)


def choose_staged_project_import(
    document: object, parent=None
) -> tuple[StagedProjectImport, set[str], StagedIOImport | None, set[str]] | None:
    """Choose a supported file and return only explicitly approved candidates.

    Project-intake candidates and CEProject logical-I/O candidates have
    separate identities.  This function never writes to ``document``; the
    command boundary applies its returned decision inside one transaction.
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
    project = existing_project_object(document)
    staged = stage_project_import(source_text, source_path, project)
    io_staged = None
    if staged.source_format == "ceproject-xml":
        io_staged = stage_ceproject_io_import(
            source_text, source_path, explicit_io_signals_from_project(project) if project is not None else ()
        )
    if not staged.candidates and not (io_staged and io_staged.candidates):
        raise RuntimeError("The import has no changed supported project fields or I/O rows to review.")

    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Review Imported Project Data")
    layout = QtWidgets.QVBoxLayout(dialog)
    layout.addWidget(QtWidgets.QLabel(
        "Select each proposed project field or logical I/O row to approve. "
        "Unchecked items are not imported."
    ))
    if staged.warnings:
        layout.addWidget(QtWidgets.QLabel("Import warnings:\n" + "\n".join(staged.warnings)))
    if io_staged is not None and io_staged.diagnostics:
        layout.addWidget(QtWidgets.QLabel(
            "I/O review findings:\n" + "\n".join(
                f"{item.severity}: {item.message}" for item in io_staged.diagnostics
            )
        ))
    approvals = {}
    for candidate in staged.candidates:
        checkbox = QtWidgets.QCheckBox(
            f"[{candidate.category}] {candidate.key}: {candidate.current_value or '<empty>'} → {candidate.proposed_value or '<empty>'}"
        )
        approvals[candidate.key] = checkbox
        layout.addWidget(checkbox)
    io_approvals = {}
    if io_staged is not None:
        for candidate in io_staged.candidates:
            current = candidate.current.description if candidate.current is not None else "<new logical I/O>"
            proposed = candidate.proposed.description if candidate.proposed is not None else "<invalid>"
            signal_type = candidate.proposed.signal_type if candidate.proposed is not None else ""
            checkbox = QtWidgets.QCheckBox(
                f"[I/O {candidate.action}] {candidate.candidate_id}: "
                f"{current} → {proposed} ({signal_type})"
            )
            if candidate.proposed is None:
                checkbox.setText(
                    f"[I/O conflict — cannot approve] {candidate.candidate_id}: {current}"
                )
                checkbox.setEnabled(False)
            io_approvals[candidate.candidate_id] = checkbox
            layout.addWidget(checkbox)
    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    execute = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if execute() != QtWidgets.QDialog.Accepted:
        return None
    return (
        staged,
        {key for key, checkbox in approvals.items() if checkbox.isChecked()},
        io_staged,
        {key for key, checkbox in io_approvals.items() if checkbox.isChecked()},
    )
