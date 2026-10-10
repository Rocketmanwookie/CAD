# SPDX-License-Identifier: MIT
"""Connection-record dialog helpers."""

from controls_wb.connections import append_connection_to_project
from controls_wb.gui.io_signal import _qt_widgets
from controls_wb.gui.project_intake import existing_project_object
from controls_wb.io_list import explicit_io_signals_from_project
from controls_wb.model.project import create_or_update_project, ensure_project_properties


def add_connection_from_form(document: object, values: dict[str, str]):
    project = existing_project_object(document) or create_or_update_project(document)
    if hasattr(project, "addProperty"):
        ensure_project_properties(project)
    return append_connection_to_project(project, values)


def allocated_connection_defaults(project: object, signal_tag: str) -> dict[str, str]:
    """Return the read-only PLC coordinates already known for ``signal_tag``.

    A connection record must not ask the user to retype the canonical placement
    chosen by allocation.  Field-device, terminal, and wire details remain
    deliberately blank because an I/O engineering label is not necessarily a
    physical field-device tag.
    """

    wanted = str(signal_tag or "").strip()
    for signal in explicit_io_signals_from_project(project):
        if signal.tag == wanted:
            return {
                "signal_tag": signal.tag,
                "plc_rack": signal.rack,
                "plc_slot": signal.slot,
                "plc_channel": signal.channel,
            }
    return {}


def selected_allocated_signal_tag(selected_objects: list[object] | tuple[object, ...] | None) -> str:
    """Resolve a selected allocated-channel object to its linked signal tag."""

    for selected in selected_objects or ():
        signal = getattr(selected, "AllocatedSignalObject", None)
        if signal is None:
            signal = selected
        tag = str(getattr(signal, "SignalTag", "") or "").strip()
        if tag:
            return tag
    return ""


def show_connection_dialog(document: object, parent=None, console=None, selected_objects=None):
    QtWidgets = _qt_widgets()
    project = existing_project_object(document) or create_or_update_project(document)
    signal_tags = [signal.tag for signal in explicit_io_signals_from_project(project)]

    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Add Connection Record")
    layout = QtWidgets.QVBoxLayout(dialog)
    form = QtWidgets.QFormLayout()
    signal_editor = QtWidgets.QComboBox()
    signal_editor.setEditable(True)
    signal_editor.addItems(signal_tags)
    editors = {"signal_tag": signal_editor}
    form.addRow("Signal tag", signal_editor)
    for key, label in (
        ("field_device", "Field device"),
        ("terminal_strip", "Terminal strip"),
        ("terminal", "Terminal"),
        ("wire_tag", "Wire tag"),
        ("plc_rack", "PLC rack"),
        ("plc_slot", "PLC slot"),
        ("plc_channel", "PLC channel"),
    ):
        editor = QtWidgets.QLineEdit()
        editors[key] = editor
        form.addRow(label, editor)

    allocated_keys = ("plc_rack", "plc_slot", "plc_channel")

    def apply_allocated_defaults(signal_tag=None):
        defaults = allocated_connection_defaults(project, signal_tag or signal_editor.currentText())
        for key in allocated_keys:
            editor = editors[key]
            editor.setText(defaults.get(key, ""))
            editor.setReadOnly(bool(defaults))

    signal_editor.currentTextChanged.connect(apply_allocated_defaults)
    selected_tag = selected_allocated_signal_tag(selected_objects)
    if selected_tag:
        signal_editor.setCurrentText(selected_tag)
    apply_allocated_defaults()
    layout.addLayout(form)
    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)
    execute = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if execute() != QtWidgets.QDialog.Accepted:
        return None
    values = {key: editor.currentText() if key == "signal_tag" else editor.text() for key, editor in editors.items()}
    connection = add_connection_from_form(document, values)
    if console is not None:
        console.PrintMessage(f"Connection record added: {connection.connection_id} for {connection.signal_tag}\n")
    return connection
