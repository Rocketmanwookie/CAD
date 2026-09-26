# SPDX-License-Identifier: MIT
"""Export canonical typed wiring and I/O path schedules."""

from pathlib import Path

try:
    import FreeCAD as App
    import FreeCADGui as Gui
except Exception:  # pragma: no cover
    App = None
    Gui = None

import csv
from io import StringIO

from controls_wb.electrical_path import io_schedule_row, wiring_schedule_rows
from controls_wb.identity import CERoles
from controls_wb.model.electrical import electrical_paths_from_project


def electrical_schedule_texts_for_objects(objects) -> tuple[str, str]:
    projects = [obj for obj in objects if hasattr(obj, "ProjectId") and hasattr(obj, "Deliverables")]
    owned_paths = []
    for obj in projects:
        if hasattr(obj, "ElectricalPaths"):
            owned_paths.extend((obj, path) for path in electrical_paths_from_project(obj))
    channels = {getattr(obj, "CEIdentity", ""): obj for obj in objects if getattr(obj, "CERole", "") == CERoles.PLC_CHANNEL}
    wiring_rows, io_rows = [], []
    for project, path in sorted(owned_paths, key=lambda item: (item[1].signal_tag, item[1].identity)):
        channel = channels.get(path.terminals[0].owner_identity)
        if channel is None:
            raise ValueError(f"Path {path.identity} PLC terminal owner is not an allocated PLC channel.")
        registered_channel_ids = {getattr(device, "CEIdentity", "") for device in (getattr(project, "ElectricalDevices", []) or []) if getattr(device, "CERole", "") == CERoles.PLC_CHANNEL}
        if getattr(channel, "CEIdentity", "") not in registered_channel_ids:
            raise ValueError(f"Path {path.identity} PLC channel is not registered on its project.")
        signal = getattr(channel, "AllocatedSignalObject", None)
        if signal is None or getattr(signal, "CEIdentity", "") != path.signal_identity:
            raise ValueError(f"Path {path.identity} does not match its allocated PLC channel signal.")
        if getattr(channel, "SignalAddress", "") != path.terminals[0].designation:
            raise ValueError(f"Path {path.identity} PLC terminal does not match allocated channel address.")
        trace = {"PLCChannelIdentity": channel.CEIdentity, "PLCRack": channel.RackNumber,
                 "PLCSlot": channel.SlotNumber, "PLCChannel": channel.ChannelNumber,
                 "PLCAddress": channel.SignalAddress}
        wiring_rows.extend(dict(row, **trace) for row in wiring_schedule_rows(path))
        io_rows.append(dict(io_schedule_row(path), **trace))
    return _csv(wiring_rows, WIRING_HEADERS), _csv(io_rows, IO_HEADERS)


WIRING_HEADERS = ("PathIdentity", "SignalIdentity", "SignalTag", "WireIdentity", "WireTag", "FromTerminalIdentity", "FromTerminal", "ToTerminalIdentity", "ToTerminal", "ConductorSize", "Color", "CircuitFunction", "ConduitIdentity", "LengthMm", "PLCChannelIdentity", "PLCRack", "PLCSlot", "PLCChannel", "PLCAddress")
IO_HEADERS = ("PathIdentity", "SignalIdentity", "SignalTag", "PLCTerminalIdentity", "PLCTerminal", "DeviceTerminalIdentity", "DeviceTerminal", "TerminalPath", "WireTags", "TotalLengthMm", "PLCChannelIdentity", "PLCRack", "PLCSlot", "PLCChannel", "PLCAddress")


def _csv(rows, headers):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=headers, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


class ExportElectricalSchedulesCommand:
    def GetResources(self):
        return {
            "MenuText": "Export Electrical Schedules",
            "ToolTip": "Export identity-safe wiring and I/O path schedules from typed electrical paths.",
        }

    def Activated(self):
        if App.ActiveDocument is None:
            App.Console.PrintWarning("No active document.\n")
            return
        try:
            wiring_text, io_text = electrical_schedule_texts_for_objects(App.ActiveDocument.Objects)
        except ValueError as exc:
            App.Console.PrintError(f"Electrical schedules were not exported: {exc}\n")
            return
        wiring_path = Path.home() / "integracad_wiring_schedule.csv"
        io_path = Path.home() / "integracad_io_path_schedule.csv"
        wiring_path.write_text(wiring_text, encoding="utf-8")
        io_path.write_text(io_text, encoding="utf-8")
        App.Console.PrintMessage(f"Wiring schedule exported to {wiring_path}\n")
        App.Console.PrintMessage(f"I/O path schedule exported to {io_path}\n")

    def IsActive(self):
        return App is not None and App.ActiveDocument is not None


if Gui is not None:
    Gui.addCommand("CE_ExportElectricalSchedules", ExportElectricalSchedulesCommand())
