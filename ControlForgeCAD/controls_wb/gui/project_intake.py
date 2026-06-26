# SPDX-License-Identifier: MIT
"""Project intake dialog helpers.

The mapping helpers in this module are pure Python. Qt imports stay inside
functions so tests and command metadata imports do not require a FreeCAD GUI.
"""

from __future__ import annotations

from dataclasses import dataclass

from controls_wb.model.project import create_or_update_project


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
    IntakeFormField("PlcPlatform", "PLC platform", "PlcPlatform"),
    IntakeFormField("SensorCount", "Sensor count", "SensorCount"),
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


def form_values_from_project(obj: object | None) -> dict[str, str]:
    values: dict[str, str] = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        value = getattr(obj, field.property_name, "") if obj is not None else ""
        values[field.key] = format_deliverables(value) if field.key == "Deliverables" else str(value or "")
    if not values["ProjectName"]:
        values["ProjectName"] = "Controls Project"
    if not values["Deliverables"]:
        values["Deliverables"] = "ioList, panelLayout"
    return values


def normalized_form_values(values: dict[str, str]) -> dict[str, object]:
    normalized: dict[str, object] = {}
    for field in CORE_INTAKE_FORM_FIELDS:
        value = values.get(field.key, "")
        normalized[field.property_name] = parse_deliverables(value) if field.key == "Deliverables" else str(value).strip()
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

    values = {key: editor.text() for key, editor in editors.items()}
    project = create_or_update_project_from_form(document, values)
    if console is not None:
        console.PrintMessage(f"Controls project intake updated: {project.ProjectName}\n")
    return project
