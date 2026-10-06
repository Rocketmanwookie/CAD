# SPDX-License-Identifier: MIT
"""Focused plant and I/O sizing steps for the workbench workflow."""

from controls_wb.gui.project_intake import (
    COMMUNICATION_PROTOCOL_OPTIONS,
    CORE_INTAKE_FORM_FIELDS,
    ENCLOSURE_RATING_OPTIONS,
    POWER_CONFIGURATIONS,
    _qt_widgets,
    existing_project_object,
    form_values_from_project,
    normalized_form_values,
)
from controls_wb.model.project import create_or_update_project


COUNT_KEYS = ("DICount", "DOCount", "AICount", "AOCount")
PLANT_PROPERTIES = (
    "ProjectName", "Customer", "SiteLocation", "Deliverables",
    "PowerConfiguration", "NominalVoltage", "PhaseCount", "ControlledLoads",
    "EstimatedLoadAmps", "EnclosureRatings", "EnclosureRating",
    "CommunicationProtocols",
)


def sizing_targets(values):
    """Validate actual counts and compute exact integer 20% capacity targets."""
    result = {}
    for key in COUNT_KEYS:
        raw = str(values.get(key, "") or "0").strip() or "0"
        if not raw.isascii() or not raw.isdecimal():
            raise ValueError(f"{key[:2]} count must be a nonnegative whole number.")
        count = int(raw)
        result[key] = (count, (count * 6 + 4) // 5)
    return result


def save_plant_questionnaire(document, values):
    """Update only plant facts; leave hardware, counts and I/O records intact."""
    normalized = normalized_form_values(values)
    project = existing_project_object(document) or create_or_update_project(document)
    for key in PLANT_PROPERTIES:
        setattr(project, key, normalized[key])
    return project


def save_io_counts(document, values):
    targets = sizing_targets(values)
    project = existing_project_object(document)
    if project is None:
        raise ValueError("Complete the Plant Questionnaire before entering I/O counts.")
    for key, (actual, _target) in targets.items():
        setattr(project, key, str(actual))
    project.SensorCount = str(targets["DICount"][0] + targets["AICount"][0])
    return project


def _buttons(widgets, dialog, layout):
    buttons = widgets.QDialogButtonBox(widgets.QDialogButtonBox.Ok | widgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)


def _accepted(dialog, widgets):
    execute = getattr(dialog, "exec_", None) or dialog.exec
    return execute() == widgets.QDialog.Accepted


def show_plant_questionnaire(document, parent=None):
    widgets = _qt_widgets()
    initial = form_values_from_project(existing_project_object(document))
    dialog = widgets.QDialog(parent)
    dialog.setWindowTitle("Project & Plant — Plant Questionnaire")
    layout = widgets.QVBoxLayout(dialog)
    form = widgets.QFormLayout()
    editors = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        editors[field.key] = widgets.QLineEdit(initial[field.key])
        form.addRow(field.label, editors[field.key])
    power = widgets.QComboBox()
    power.addItems(list(POWER_CONFIGURATIONS))
    power.setCurrentText(initial["PowerConfiguration"] or "3PH 480V")
    form.addRow("Plant supply", power)
    loads = widgets.QTextEdit()
    loads.setPlainText(initial["ControlledLoads"])
    loads.setPlaceholderText("motor, Conveyor motor, 1, 1.5hp")
    form.addRow("Controlled loads", loads)
    enclosure = widgets.QLineEdit(initial["EnclosureRatings"])
    enclosure.setPlaceholderText(", ".join(ENCLOSURE_RATING_OPTIONS))
    form.addRow("Enclosure requirements", enclosure)
    protocols = widgets.QLineEdit(initial["CommunicationProtocols"])
    protocols.setPlaceholderText(", ".join(COMMUNICATION_PROTOCOL_OPTIONS))
    form.addRow("Network protocols", protocols)
    layout.addLayout(form)
    _buttons(widgets, dialog, layout)
    while _accepted(dialog, widgets):
        values = {key: editor.text() for key, editor in editors.items()}
        values.update(PowerConfiguration=power.currentText(), ControlledLoads=loads.toPlainText(),
                      EnclosureRatings=enclosure.text(), CommunicationProtocols=protocols.text())
        try:
            return save_plant_questionnaire(document, values)
        except ValueError as exc:
            widgets.QMessageBox.warning(dialog, "Plant questionnaire", str(exc))
    return None


def show_io_count_dialog(document, parent=None):
    widgets = _qt_widgets()
    project = existing_project_object(document)
    if project is None:
        raise ValueError("Complete the Plant Questionnaire before entering I/O counts.")
    dialog = widgets.QDialog(parent)
    dialog.setWindowTitle("Controls Circuit — I/O Count")
    layout = widgets.QVBoxLayout(dialog)
    form = widgets.QFormLayout()
    editors = {}
    for key in COUNT_KEYS:
        editors[key] = widgets.QLineEdit(str(getattr(project, key, "") or "0"))
        form.addRow(f"Required {key[:2]} points", editors[key])
    layout.addLayout(form)
    summary = widgets.QLabel()
    layout.addWidget(summary)
    layout.addWidget(widgets.QLabel("Next: select PLC and modules, then define the actual I/O points."))

    def refresh(_text=None):
        try:
            targets = sizing_targets({key: editor.text() for key, editor in editors.items()})
            summary.setText("Capacity including 20% spare: " + "; ".join(
                f"{key[:2]} {target} ({target - actual} spare)"
                for key, (actual, target) in targets.items()))
        except ValueError as exc:
            summary.setText(str(exc))

    for editor in editors.values():
        editor.textChanged.connect(refresh)
    refresh()
    _buttons(widgets, dialog, layout)
    while _accepted(dialog, widgets):
        try:
            return save_io_counts(document, {key: editor.text() for key, editor in editors.items()})
        except ValueError as exc:
            widgets.QMessageBox.warning(dialog, "I/O count", str(exc))
    return None
