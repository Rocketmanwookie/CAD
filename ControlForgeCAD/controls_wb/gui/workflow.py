# SPDX-License-Identifier: MIT
"""Focused plant and I/O sizing steps for the workbench workflow."""

from types import SimpleNamespace

from controls_wb.gui.project_intake import (
    COMMUNICATION_PROTOCOL_OPTIONS,
    CORE_INTAKE_FORM_FIELDS,
    ENCLOSURE_RATING_OPTIONS,
    POWER_CONFIGURATIONS,
    _qt_widgets,
    existing_project_object,
    form_values_from_project,
    normalized_form_values,
    parse_multiselect,
)
from controls_wb.model.project import create_or_update_project
from controls_wb.hardware_catalog import load_hardware_catalog, makes, lines_for_make, recommend_plc_hardware
from controls_wb.io_list import explicit_io_signals_from_project, io_allocation_for_project, serialize_io_signal
from controls_wb.allocation_reconciliation import preflight_reconciliation
from controls_wb.model.layout import materialize_plc_allocation
from controls_wb.gui.allocation_review import show_allocation_naming_dialog


def configuration_preview(project, make, line, cpu):
    """Compute a spare-aware allocation without changing the document."""
    candidate = SimpleNamespace(**{
        key: getattr(project, key, default)
        for key, default in (("ProjectId", ""), ("ProjectName", ""),
                             ("Deliverables", []), ("IOSignals", []), ("SourceRecords", []),
                             ("SensorCount", ""), *( (key, "") for key in COUNT_KEYS ))
    })
    candidate.PlcMake, candidate.PlcLine, candidate.PlcCPU = make, line, cpu
    sizing_targets({key: getattr(candidate, key) for key in COUNT_KEYS})
    preview = io_allocation_for_project(candidate)
    if preview is None:
        raise ValueError("Select a PLC make, line and CPU.")
    errors = [finding.message for finding in preview.findings if finding.severity == "ERROR"]
    if errors:
        raise ValueError("; ".join(errors))
    dependent_tags = {
        str(getattr(getattr(path, "SignalObject", None), "SignalTag", "") or "")
        for path in (getattr(project, "ElectricalPaths", []) or [])
    }
    preflight_reconciliation(explicit_io_signals_from_project(project), preview.signals, dependent_tags)
    return preview


def save_plc_configuration(document, make, line, cpu):
    project = existing_project_object(document)
    if project is None:
        raise ValueError("Complete the Plant Questionnaire and I/O Count first.")
    preview = configuration_preview(project, make, line, cpu)
    project.PlcMake, project.PlcLine, project.PlcCPU = make, line, cpu
    project.PlcPlatform = f"{make} {line}"
    project.IOSignals = [serialize_io_signal(signal) for signal in preview.signals]
    if callable(getattr(document, "addObject", None)):
        materialize_plc_allocation(document, project)
    return project


def show_define_io(document, parent=None):
    project = existing_project_object(document)
    if project is None or not getattr(project, "IOSignals", []):
        raise ValueError("Save the PLC configuration before defining I/O labels.")
    preview = configuration_preview(project, project.PlcMake, project.PlcLine, project.PlcCPU)
    approved = show_allocation_naming_dialog(preview, parent)
    if approved is None:
        return None
    project.IOSignals = [serialize_io_signal(signal) for signal in approved.signals]
    if callable(getattr(document, "addObject", None)):
        materialize_plc_allocation(document, project)
    return project


COUNT_KEYS = ("DICount", "DOCount", "AICount", "AOCount")
PLANT_PROPERTIES = (
    "ProjectName", "Customer", "SiteLocation",
    "PowerConfiguration", "NominalVoltage", "PhaseCount", "ControlledLoads",
    "EstimatedLoadAmps", "EnclosureRatings", "EnclosureRating",
    "CommunicationProtocols",
)
PLANT_FORM_FIELDS = tuple(field for field in CORE_INTAKE_FORM_FIELDS if field.key != "Deliverables")


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


def _checkbox_group(widgets, options, selected_values):
    """Build a compact multi-select control from the stored list value."""

    selected = set(parse_multiselect(selected_values))
    container = widgets.QWidget()
    layout = widgets.QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    boxes = []
    for option in options:
        box = widgets.QCheckBox(option)
        box.setChecked(option in selected)
        layout.addWidget(box)
        boxes.append(box)
    return container, boxes


def _checked_options(boxes):
    return [box.text() for box in boxes if box.isChecked()]


def show_plant_questionnaire(document, parent=None):
    widgets = _qt_widgets()
    initial = form_values_from_project(existing_project_object(document))
    dialog = widgets.QDialog(parent)
    dialog.setWindowTitle("Project & Plant — Plant Questionnaire")
    layout = widgets.QVBoxLayout(dialog)
    form = widgets.QFormLayout()
    editors = {}
    for field in PLANT_FORM_FIELDS:
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
    enclosure, enclosure_boxes = _checkbox_group(
        widgets, ENCLOSURE_RATING_OPTIONS, initial["EnclosureRatings"]
    )
    form.addRow("Enclosure requirements", enclosure)
    protocols, protocol_boxes = _checkbox_group(
        widgets, COMMUNICATION_PROTOCOL_OPTIONS, initial["CommunicationProtocols"]
    )
    form.addRow("Network protocols", protocols)
    layout.addLayout(form)
    _buttons(widgets, dialog, layout)
    while _accepted(dialog, widgets):
        values = {key: editor.text() for key, editor in editors.items()}
        values.update(PowerConfiguration=power.currentText(), ControlledLoads=loads.toPlainText(),
                      EnclosureRatings=_checked_options(enclosure_boxes),
                      CommunicationProtocols=_checked_options(protocol_boxes))
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


def show_plc_configurator(document, parent=None):
    widgets = _qt_widgets()
    project = existing_project_object(document)
    if project is None:
        raise ValueError("Complete the Plant Questionnaire and I/O Count first.")
    catalog = load_hardware_catalog()
    dialog = widgets.QDialog(parent)
    dialog.setWindowTitle("Controls Circuit — PLC Configurator")
    layout = widgets.QVBoxLayout(dialog)
    form = widgets.QFormLayout()
    make = widgets.QComboBox()
    make.addItems(list(makes(catalog)))
    make.setCurrentText(str(getattr(project, "PlcMake", "") or "Siemens"))
    line = widgets.QComboBox()
    cpu = widgets.QComboBox()
    form.addRow("PLC make", make)
    form.addRow("PLC family", line)
    form.addRow("CPU (capacity including 20% spare)", cpu)
    layout.addLayout(form)
    summary = widgets.QLabel()
    layout.addWidget(summary)
    recommendations = []

    def refresh_preview(_index=None):
        if cpu.currentIndex() < 0:
            summary.setText("No catalog configuration covers the current demand and 20% spare. Revise I/O Count or platform.")
            return
        recommendation = recommendations[cpu.currentIndex()]
        try:
            preview = configuration_preview(project, make.currentText(), line.currentText(), recommendation.cpu.name)
            summary.setText("Capacity targets: " + ", ".join(
                f"{key.upper()} {target}" for key, target in recommendation.target_counts)
                + "\n\nHardware to install:\n" + "\n".join(
                    f"Slot {module.slot}: {module.module_name} — {module.part_number}"
                    for module in preview.modules)
                + f"\n\n{len(preview.signals)} actual I/O points; unused capacity remains spare."
                + "\nSave configures and allocates hardware. Define I/O labels next.")
        except ValueError as exc:
            summary.setText(str(exc))

    def refresh_cpus(_text=None):
        nonlocal recommendations
        cpu.blockSignals(True)
        cpu.clear()
        actual = {key: getattr(project, key, "") for key in COUNT_KEYS}
        try:
            sizing_targets(actual)
            # Explicit definitions may exceed the initial estimates. Size for
            # both so imported/defined points are never dropped from the plan.
            explicit = explicit_io_signals_from_project(project)
            counts = [max(int(str(actual[key] or "0")), sum(s.signal_type == kind for s in explicit))
                      for key, kind in zip(COUNT_KEYS, ("digital_input", "digital_output", "analog_input", "analog_output"))]
            recommendations = list(recommend_plc_hardware(catalog, make.currentText(), line.currentText(), *counts))
            cpu.addItems([item.cpu.name for item in recommendations])
            cpu.setCurrentText(str(getattr(project, "PlcCPU", "") or ""))
        except ValueError:
            recommendations = []
        cpu.blockSignals(False)
        refresh_preview()

    def refresh_lines(_text=None):
        line.blockSignals(True)
        line.clear()
        line.addItems(list(lines_for_make(catalog, make.currentText())))
        line.setCurrentText(str(getattr(project, "PlcLine", "") or ""))
        line.blockSignals(False)
        refresh_cpus()

    make.currentTextChanged.connect(refresh_lines)
    line.currentTextChanged.connect(refresh_cpus)
    cpu.currentIndexChanged.connect(refresh_preview)
    refresh_lines()
    _buttons(widgets, dialog, layout)
    while _accepted(dialog, widgets):
        if cpu.currentIndex() < 0:
            widgets.QMessageBox.warning(dialog, "PLC configurator", "No feasible configuration is selected.")
            continue
        try:
            configuration_preview(project, make.currentText(), line.currentText(), recommendations[cpu.currentIndex()].cpu.name)
        except ValueError as exc:
            widgets.QMessageBox.warning(dialog, "PLC configurator", str(exc))
            continue
        # Let materialization failures reach the command transaction so the
        # complete hardware/record change is aborted rather than retried over
        # partially changed state.
        return save_plc_configuration(document, make.currentText(), line.currentText(), recommendations[cpu.currentIndex()].cpu.name)
    return None
