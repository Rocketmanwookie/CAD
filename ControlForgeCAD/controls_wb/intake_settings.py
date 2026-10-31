# SPDX-License-Identifier: MIT
"""Per-user settings for the local job-intake workflow."""

from dataclasses import dataclass

PREFERENCES_PATH = "User parameter:BaseApp/Preferences/Mod/ControlForgeCAD/Intake"
DELIVERY_METHODS = ("local_form", "email_draft", "delivery_url")
DELIVERY_METHOD_LABELS = {
    "local_form": "Open local intake form",
    "email_draft": "Prepare email draft",
    "delivery_url": "Open delivery URL",
}


@dataclass(frozen=True)
class IntakeSystemSettings:
    database_location: str = "~/ControlForgeCAD/intake.sqlite"
    delivery_method: str = "local_form"
    delivery_target: str = ""
    form_template: str = ""

    def normalized(self) -> "IntakeSystemSettings":
        settings = IntakeSystemSettings(
            database_location=self.database_location.strip(),
            delivery_method=self.delivery_method.strip(),
            delivery_target=self.delivery_target.strip(),
            form_template=self.form_template.strip(),
        )
        if not settings.database_location:
            raise ValueError("Enter a local intake database location.")
        if settings.delivery_method not in DELIVERY_METHODS:
            raise ValueError("Select a supported form-delivery method.")
        return settings


def _preferences(app):
    if app is None:
        try:
            import FreeCAD as app
        except Exception as exc:  # pragma: no cover - FreeCAD supplies this in production.
            raise RuntimeError("FreeCAD user preferences are unavailable.") from exc
    return app.ParamGet(PREFERENCES_PATH)


def load_intake_settings(app=None) -> IntakeSystemSettings:
    """Load local intake preferences without creating a database or delivery."""
    preferences = _preferences(app)
    return IntakeSystemSettings(
        database_location=preferences.GetString("DatabaseLocation", "~/ControlForgeCAD/intake.sqlite"),
        delivery_method=preferences.GetString("DeliveryMethod", "local_form"),
        delivery_target=preferences.GetString("DeliveryTarget", ""),
        form_template=preferences.GetString("FormTemplate", ""),
    ).normalized()


def save_intake_settings(settings: IntakeSystemSettings, app=None) -> IntakeSystemSettings:
    """Validate and store local intake preferences in FreeCAD's user settings."""
    normalized = settings.normalized()
    preferences = _preferences(app)
    preferences.SetString("DatabaseLocation", normalized.database_location)
    preferences.SetString("DeliveryMethod", normalized.delivery_method)
    preferences.SetString("DeliveryTarget", normalized.delivery_target)
    preferences.SetString("FormTemplate", normalized.form_template)
    return normalized


def show_intake_system_settings(parent=None):
    """Display and persist the local intake settings dialog."""
    from controls_wb.gui.io_signal import _qt_widgets

    widgets = _qt_widgets()
    settings = load_intake_settings()
    dialog = widgets.QDialog(parent)
    dialog.setWindowTitle("Job Intake & Database Settings")
    layout = widgets.QVBoxLayout(dialog)
    form = widgets.QFormLayout()

    database_location = widgets.QLineEdit(settings.database_location)
    database_location.setPlaceholderText("~/ControlForgeCAD/intake.sqlite")
    form.addRow("Local intake database", database_location)

    delivery_method = widgets.QComboBox()
    for method in DELIVERY_METHODS:
        delivery_method.addItem(DELIVERY_METHOD_LABELS[method], method)
    delivery_method.setCurrentIndex(DELIVERY_METHODS.index(settings.delivery_method))
    form.addRow("Form delivery", delivery_method)

    delivery_target = widgets.QLineEdit(settings.delivery_target)
    delivery_target.setPlaceholderText("Email address or delivery URL, if applicable")
    form.addRow("Delivery target", delivery_target)

    form_template = widgets.QLineEdit(settings.form_template)
    form_template.setPlaceholderText("Optional local form template path")
    form.addRow("Form template", form_template)
    layout.addLayout(form)

    boundary = widgets.QLabel(
        "These are local workstation preferences. They do not create a database, send email, "
        "or transmit project data; the current intake form and database console remain local FreeCAD workflows."
    )
    boundary.setWordWrap(True)
    layout.addWidget(boundary)

    buttons = widgets.QDialogButtonBox(widgets.QDialogButtonBox.Ok | widgets.QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    layout.addWidget(buttons)

    execute = getattr(dialog, "exec_", None) or dialog.exec
    while execute() == widgets.QDialog.Accepted:
        try:
            return save_intake_settings(
                IntakeSystemSettings(
                    database_location=database_location.text(),
                    delivery_method=delivery_method.currentData(),
                    delivery_target=delivery_target.text(),
                    form_template=form_template.text(),
                )
            )
        except ValueError as exc:
            widgets.QMessageBox.warning(dialog, "Job Intake & Database Settings", str(exc))
    return None
