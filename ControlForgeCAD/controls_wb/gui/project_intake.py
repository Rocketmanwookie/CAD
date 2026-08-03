# SPDX-License-Identifier: MIT
"""Project intake dialog helpers.

The mapping helpers in this module are pure Python. Qt imports stay inside
functions so tests and command metadata imports do not require a FreeCAD GUI.
"""

from __future__ import annotations

from dataclasses import dataclass

from controls_wb.model.project import create_or_update_project, ensure_project_properties

PLC_LINES_BY_MAKE = {
    "Siemens": ("S7-1200", "S7-1500", "ET 200SP"),
    "Allen-Bradley": ("Micro800", "CompactLogix 5380", "ControlLogix 5580"),
}

IO_ACCESSORY_OPTIONS = (
    "Remote / modular I/O bank",
    "Ethernet I/O adapter",
    "I/O terminal bases",
    "Expansion power supply",
)


@dataclass(frozen=True)
class IntakeFormField:
    key: str
    label: str
    property_name: str


CORE_INTAKE_FORM_FIELDS = (
    IntakeFormField("ProjectName", "Project name", "ProjectName"),
    IntakeFormField("Customer", "Customer", "Customer"),
    IntakeFormField("SiteLocation", "Site/location", "SiteLocation"),
    IntakeFormField("Deliverables", "Deliverables", "Deliverables"),
    IntakeFormField("NominalVoltage", "Nominal voltage", "NominalVoltage"),
    IntakeFormField("PhaseCount", "Phase count", "PhaseCount"),
    IntakeFormField("EnclosureRating", "Enclosure rating", "EnclosureRating"),
)

PLC_IO_FORM_FIELDS = (
    IntakeFormField("PlcMake", "PLC make", "PlcMake"),
    IntakeFormField("PlcLine", "PLC line", "PlcLine"),
    IntakeFormField("DICount", "DI count", "DICount"),
    IntakeFormField("DOCount", "DO count", "DOCount"),
    IntakeFormField("AICount", "AI count", "AICount"),
    IntakeFormField("AOCount", "AO count", "AOCount"),
    IntakeFormField("IOAccessories", "I/O accessories", "IOAccessories"),
)


def parse_deliverables(value: str | list[str] | tuple[str, ...] | set[str]) -> list[str]:
    if isinstance(value, str):
        raw_items = value.split(",")
    else:
        raw_items = list(value)
    return sorted({str(item).strip() for item in raw_items if str(item).strip()})


def format_deliverables(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return ", ".join(parse_deliverables(value))
    if isinstance(value, (list, tuple, set)):
        return ", ".join(parse_deliverables(value))
    return str(value)


def parse_accessories(value: str | list[str] | tuple[str, ...] | set[str]) -> list[str]:
    return parse_deliverables(value)


def format_accessories(value: object) -> str:
    return format_deliverables(value)


def plc_lines_for_make(make: str) -> tuple[str, ...]:
    return PLC_LINES_BY_MAKE.get(make, ())


def normalized_plc_line(make: str, line: str) -> str:
    lines = plc_lines_for_make(make)
    clean_line = str(line).strip()
    if clean_line in lines:
        return clean_line
    return lines[0] if lines else clean_line


def plc_platform_from_make_line(make: str, line: str) -> str:
    clean_make = str(make).strip()
    clean_line = str(line).strip()
    return " ".join(part for part in (clean_make, clean_line) if part)


def _safe_count(value: object) -> str:
    try:
        count = int(str(value).strip())
    except (TypeError, ValueError):
        return ""
    return str(max(count, 0))


def total_input_count(di_count: object, ai_count: object) -> str:
    total = int(_safe_count(di_count) or "0") + int(_safe_count(ai_count) or "0")
    return str(total) if total else ""


def form_values_from_project(obj: object | None) -> dict[str, str]:
    values: dict[str, str] = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        value = getattr(obj, field.property_name, "") if obj is not None else ""
        values[field.key] = format_deliverables(value) if field.key == "Deliverables" else str(value or "")
    for field in PLC_IO_FORM_FIELDS:
        value = getattr(obj, field.property_name, "") if obj is not None else ""
        values[field.key] = format_accessories(value) if field.key == "IOAccessories" else str(value or "")
    if not values["ProjectName"]:
        values["ProjectName"] = "Controls Project"
    if not values["Deliverables"]:
        values["Deliverables"] = "ioList, panelLayout"
    if not values["PlcMake"]:
        platform = str(getattr(obj, "PlcPlatform", "") if obj is not None else "")
        values["PlcMake"] = "Allen-Bradley" if "Allen" in platform or "ControlLogix" in platform or "CompactLogix" in platform else "Siemens"
    values["PlcLine"] = normalized_plc_line(values["PlcMake"], values["PlcLine"])
    return values


def normalized_form_values(values: dict[str, str]) -> dict[str, object]:
    normalized: dict[str, object] = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        value = values.get(field.key, "")
        normalized[field.property_name] = parse_deliverables(value) if field.key == "Deliverables" else str(value).strip()
    plc_make = str(values.get("PlcMake", "Siemens")).strip() or "Siemens"
    if plc_make not in PLC_LINES_BY_MAKE:
        plc_make = "Siemens"
    plc_line = normalized_plc_line(plc_make, values.get("PlcLine", ""))
    normalized["PlcMake"] = plc_make
    normalized["PlcLine"] = plc_line
    normalized["PlcPlatform"] = plc_platform_from_make_line(plc_make, plc_line)
    normalized["DICount"] = _safe_count(values.get("DICount", ""))
    normalized["DOCount"] = _safe_count(values.get("DOCount", ""))
    normalized["AICount"] = _safe_count(values.get("AICount", ""))
    normalized["AOCount"] = _safe_count(values.get("AOCount", ""))
    normalized["SensorCount"] = total_input_count(normalized["DICount"], normalized["AICount"])
    normalized["IOAccessories"] = parse_accessories(values.get("IOAccessories", ""))
    if not normalized["ProjectName"]:
        normalized["ProjectName"] = "Controls Project"
    return normalized


def apply_form_values_to_project(obj: object, values: dict[str, str]) -> object:
    for property_name, value in normalized_form_values(values).items():
        setattr(obj, property_name, value)
    return obj


def existing_project_object(document: object) -> object | None:
    for obj in getattr(document, "Objects", []) or []:
        if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables"):
            return obj
    return None


def create_or_update_project_from_form(document: object, values: dict[str, str]) -> object:
    normalized = normalized_form_values(values)
    obj = existing_project_object(document)
    if obj is not None:
        if hasattr(obj, "addProperty"):
            ensure_project_properties(obj)
    else:
        obj = create_or_update_project(document, name=str(normalized["ProjectName"]))
    for property_name, value in normalized.items():
        setattr(obj, property_name, value)
    return obj


def _qt_widgets():
    errors = []
    for module_name in ("PySide.QtGui", "PySide2.QtWidgets", "PySide6.QtWidgets"):
        try:
            module = __import__(module_name, fromlist=["QtWidgets"])
            if module_name == "PySide.QtGui":
                return module
            return module
        except Exception as exc:  # pragma: no cover - depends on FreeCAD Qt runtime
            errors.append(exc)
    raise RuntimeError("Qt/PySide is unavailable.") from errors[-1] if errors else None


def show_project_intake_dialog(document: object, parent=None, console=None) -> object | None:
    """Show a modal project intake dialog and create/update CE_Project on submit."""
    QtWidgets = _qt_widgets()
    existing = existing_project_object(document)
    initial_values = form_values_from_project(existing)

    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle("Project Intake")
    layout = QtWidgets.QVBoxLayout(dialog)
    form = QtWidgets.QFormLayout()
    editors = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        editor = QtWidgets.QLineEdit(initial_values[field.key])
        editors[field.key] = editor
        form.addRow(field.label, editor)
    make_editor = QtWidgets.QComboBox()
    make_editor.addItems(list(PLC_LINES_BY_MAKE.keys()))
    make_editor.setCurrentText(initial_values["PlcMake"])
    line_editor = QtWidgets.QComboBox()

    def refresh_lines():
        current_line = line_editor.currentText() or initial_values["PlcLine"]
        line_editor.clear()
        line_editor.addItems(list(plc_lines_for_make(make_editor.currentText())))
        line_editor.setCurrentText(normalized_plc_line(make_editor.currentText(), current_line))

    make_editor.currentTextChanged.connect(lambda _text: refresh_lines())
    refresh_lines()
    editors["PlcMake"] = make_editor
    editors["PlcLine"] = line_editor
    form.addRow("PLC make", make_editor)
    form.addRow("PLC line", line_editor)

    for field in PLC_IO_FORM_FIELDS:
        if field.key in {"PlcMake", "PlcLine", "IOAccessories"}:
            continue
        editor = QtWidgets.QLineEdit(initial_values[field.key])
        editors[field.key] = editor
        form.addRow(field.label, editor)

    accessory_editors = {}
    accessory_box = QtWidgets.QWidget()
    accessory_layout = QtWidgets.QVBoxLayout(accessory_box)
    selected_accessories = set(parse_accessories(initial_values["IOAccessories"]))
    for accessory in IO_ACCESSORY_OPTIONS:
        checkbox = QtWidgets.QCheckBox(accessory)
        checkbox.setChecked(accessory in selected_accessories)
        accessory_editors[accessory] = checkbox
        accessory_layout.addWidget(checkbox)
    layout.addLayout(form)
    layout.addWidget(accessory_box)

    buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
    )
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    exec_dialog = getattr(dialog, "exec_", None) or getattr(dialog, "exec")
    if exec_dialog() != QtWidgets.QDialog.Accepted:
        return None

    values = {}
    for key, editor in editors.items():
        if hasattr(editor, "currentText"):
            values[key] = editor.currentText()
        else:
            values[key] = editor.text()
    values["IOAccessories"] = [
        accessory
        for accessory, checkbox in accessory_editors.items()
        if checkbox.isChecked()
    ]
    project = create_or_update_project_from_form(document, values)
    if console is not None:
        console.PrintMessage(f"Controls project intake updated: {project.ProjectName}\n")
    return project
