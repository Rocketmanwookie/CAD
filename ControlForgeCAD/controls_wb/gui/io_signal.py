# SPDX-License-Identifier: MIT
"""I/O signal entry dialog helpers."""

from __future__ import annotations

from controls_wb.io_list import (
    IO_SIGNAL_TYPES,
    append_io_signal_to_project,
    io_signal_type_key_from_label,
    io_signal_type_labels,
)
from controls_wb.gui.project_intake import existing_project_object
from controls_wb.model.project import create_or_update_project, ensure_project_properties


def normalized_io_signal_form_values(values: dict[str, str]) -> dict[str, str]:
    label = str(values.get("Label", "")).strip()
    type_label = str(values.get("SignalType", "")).strip() or IO_SIGNAL_TYPES[0].label
    return {
        "SignalType": io_signal_type_key_from_label(type_label),
        "Label": label,
    }


def add_io_signal_from_form(document: object, values: dict[str, str]) -> object:
    project = existing_project_object(document) or create_or_update_project(document)
    if hasattr(project, "addProperty"):
        ensure_project_properties(project)
    normalized = normalized_io_signal_form_values(values)
    return append_io_signal_to_project(
        project,
        normalized["SignalType"],
        normalized["Label"],
    )


def _qt_widgets():
    errors = []
    for module_name in ("PySide.QtGui", "PySide2.QtWidgets", "PySide6.QtWidgets"):
        try:
            module = __import__(module_name, fromlist=["QtWidgets"])
            return module
        except Exception as exc:  # pragma: no cover - depends on FreeCAD Qt runtime
            errors.append(exc)
    raise RuntimeError("Qt/PySide is unavailable.") from errors[-1] if errors else None


def show_io_signal_dialog(document: object, parent=None, console=None) -> object | None:
    """Show a modal I/O signal dialog and append a signal to CE_Project."""
    QtWidgets = _qt_widgets()

    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Add I/O Signal")
    layout = QtWidgets.QVBoxLayout(dialog)
    form = QtWidgets.QFormLayout()

    type_editor = QtWidgets.QComboBox()
    type_editor.addItems(list(io_signal_type_labels()))
    label_editor = QtWidgets.QLineEdit()

    form.addRow("I/O type", type_editor)
    form.addRow("Label", label_editor)
    layout.addLayout(form)

    buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
    )
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    exec_dialog = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if exec_dialog() != QtWidgets.QDialog.Accepted:
        return None

    signal = add_io_signal_from_form(
        document,
        {
            "SignalType": type_editor.currentText(),
            "Label": label_editor.text(),
        },
    )
    if console is not None:
        console.PrintMessage(f"I/O signal added: {signal.tag} {signal.description} ({signal.address})\n")
    return signal
