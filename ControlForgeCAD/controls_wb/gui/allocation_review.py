# SPDX-License-Identifier: MIT
"""Explicit review dialog for deterministic catalog I/O allocation rows."""

from controls_wb.io_allocation import IOAllocationResult, allocation_preview_rows, apply_engineering_labels


def _qt_widgets():
    errors = []
    for module_name in ("PySide.QtGui", "PySide2.QtWidgets", "PySide6.QtWidgets"):
        try:
            return __import__(module_name, fromlist=["QtWidgets"])
        except Exception as exc:  # pragma: no cover - depends on FreeCAD Qt runtime
            errors.append(exc)
    raise RuntimeError("Qt/PySide is unavailable.") from errors[-1] if errors else None


def show_allocation_naming_dialog(
    allocation: IOAllocationResult, parent=None
) -> IOAllocationResult | None:
    """Review catalog rows and approve readable labels without editing keys."""

    QtWidgets = _qt_widgets()
    rows = allocation_preview_rows(allocation)
    if not rows:
        raise ValueError("The proposed allocation has no catalog channel rows to review.")
    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Review Allocated I/O Channels")
    layout = QtWidgets.QVBoxLayout(dialog)
    layout.addWidget(QtWidgets.QLabel(
        "Catalog part, rack, slot, channel, and PLC terminal are canonical and read-only. "
        "Enter a readable engineering label for each I/O point."
    ))
    form = QtWidgets.QFormLayout()
    label_editors = {}
    for row in rows:
        key = (
            f"{row.signal_tag} — {row.module_name} ({row.part_number}), "
            f"R{row.rack} S{row.slot} C{row.channel}, {row.plc_terminal}"
        )
        editor = QtWidgets.QLineEdit(row.engineering_label)
        label_editors[row.signal_tag] = editor
        form.addRow(key, editor)
    layout.addLayout(form)
    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    execute = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if execute() != QtWidgets.QDialog.Accepted:
        return None
    return apply_engineering_labels(
        allocation, {tag: editor.text() for tag, editor in label_editors.items()}
    )
