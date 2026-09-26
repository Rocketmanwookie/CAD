# SPDX-License-Identifier: MIT
"""Starter controls layout objects for FreeCAD documents."""

from __future__ import annotations

from dataclasses import dataclass, replace

from controls_wb.hardware_catalog import default_catalog_path, line_catalog, load_hardware_catalog, part_by_name
from controls_wb.identity import CERoles, ensure_object_identity, imported_ce_identity
from controls_wb.panel_hardware_catalog import (
    default_panel_catalog_path,
    load_panel_hardware_catalog,
    part_for_layout,
)

try:
    import FreeCAD as App
    import Part
except Exception:  # pragma: no cover
    App = None
    Part = None


@dataclass(frozen=True)
class LayoutObjectSpec:
    name: str
    role: str
    tag: str
    description: str
    panel_name: str
    width: str
    height: str
    depth: str
    manufacturer: str = ""
    part_number: str = ""
    voltage: str = ""
    current: str = ""
    terminal_count: int = 0
    slot_number: int = 0
    channel_count: int = 0
    signal_type: str = ""
    cad_model_path: str = ""
    cad_model_format: str = ""
    cad_model_sha256: str = ""


STARTER_LAYOUT_SPECS = (
    LayoutObjectSpec(
        name="CE_Backplate",
        role=CERoles.PANEL,
        tag="PANEL-001",
        description="Control panel enclosure/backplate placeholder",
        panel_name="PANEL-001",
        width="800 mm",
        height="1000 mm",
        depth="3 mm",
    ),
    LayoutObjectSpec(
        name="CE_DIN_Rail",
        role=CERoles.MOUNTING_RAIL,
        tag="DIN-001",
        description="DIN rail placeholder",
        panel_name="PANEL-001",
        width="600 mm",
        height="35 mm",
        depth="7.5 mm",
    ),
    LayoutObjectSpec(
        name="CE_Wire_Duct",
        role=CERoles.WIRE_DUCT,
        tag="DUCT-001",
        description="Wire duct placeholder",
        panel_name="PANEL-001",
        width="600 mm",
        height="80 mm",
        depth="60 mm",
    ),
    LayoutObjectSpec(
        name="CE_Terminal_Strip",
        role=CERoles.TERMINAL_STRIP,
        tag="TB-001",
        description="Terminal strip placeholder",
        panel_name="PANEL-001",
        width="300 mm",
        height="45 mm",
        depth="50 mm",
        terminal_count=16,
    ),
    LayoutObjectSpec(
        name="CE_PLC_Rack",
        role=CERoles.PLC_CONTROLLER,
        tag="PLC-001",
        description="PLC rack/module placeholder",
        panel_name="PANEL-001",
        width="250 mm",
        height="120 mm",
        depth="90 mm",
        voltage="24 VDC",
        current="2 A",
        slot_number=0,
        channel_count=16,
        signal_type="mixed_io",
    ),
)


LAYOUT_PROPERTY_SPECS = (
    ("App::PropertyString", "Tag", "Controls", "Device tag"),
    ("App::PropertyString", "Manufacturer", "Controls", "Manufacturer"),
    ("App::PropertyString", "PartNumber", "Controls", "Part number"),
    ("App::PropertyString", "Description", "Controls", "Description"),
    ("App::PropertyString", "PanelName", "Controls", "Panel name"),
    ("App::PropertyString", "Voltage", "Electrical", "Nominal voltage"),
    ("App::PropertyString", "Current", "Electrical", "Nominal current"),
    ("App::PropertyInteger", "TerminalCount", "Controls", "Terminal count"),
    ("App::PropertyInteger", "SlotNumber", "Controls", "PLC slot number"),
    ("App::PropertyInteger", "ChannelCount", "Controls", "I/O channel count"),
    ("App::PropertyString", "SignalType", "Controls", "Signal type"),
    ("App::PropertyString", "CadModelPath", "CADbase", "Referenced CAD model path"),
    ("App::PropertyString", "CadModelFormat", "CADbase", "Referenced CAD model format"),
    ("App::PropertyString", "CadModelSha256", "CADbase", "Referenced CAD model SHA-256"),
    ("App::PropertyLength", "Width", "Geometry", "Placeholder width"),
    ("App::PropertyLength", "Height", "Geometry", "Placeholder height"),
    ("App::PropertyLength", "Depth", "Geometry", "Placeholder depth"),
)


def ensure_layout_properties(obj) -> None:
    existing = set(getattr(obj, "PropertiesList", []) or [])
    for property_type, name, group, description in LAYOUT_PROPERTY_SPECS:
        if name not in existing:
            obj.addProperty(property_type, name, group, description)


def apply_layout_spec(obj, spec: LayoutObjectSpec):
    obj.Tag = spec.tag
    obj.Manufacturer = spec.manufacturer
    obj.PartNumber = spec.part_number
    obj.Description = spec.description
    obj.PanelName = spec.panel_name
    obj.Voltage = spec.voltage
    obj.Current = spec.current
    obj.TerminalCount = spec.terminal_count
    obj.SlotNumber = spec.slot_number
    obj.ChannelCount = spec.channel_count
    obj.SignalType = spec.signal_type
    obj.CadModelPath = spec.cad_model_path
    obj.CadModelFormat = spec.cad_model_format
    obj.CadModelSha256 = spec.cad_model_sha256
    obj.Width = spec.width
    obj.Height = spec.height
    obj.Depth = spec.depth
    return obj


def layout_object_metadata(obj) -> dict[str, object]:
    return {
        "CEIdentity": getattr(obj, "CEIdentity", ""),
        "CERole": getattr(obj, "CERole", ""),
        "Tag": getattr(obj, "Tag", ""),
        "Manufacturer": getattr(obj, "Manufacturer", ""),
        "PartNumber": getattr(obj, "PartNumber", ""),
        "Description": getattr(obj, "Description", ""),
        "PanelName": getattr(obj, "PanelName", ""),
        "Voltage": getattr(obj, "Voltage", ""),
        "Current": getattr(obj, "Current", ""),
        "TerminalCount": getattr(obj, "TerminalCount", 0),
        "SlotNumber": getattr(obj, "SlotNumber", 0),
        "ChannelCount": getattr(obj, "ChannelCount", 0),
        "SignalType": getattr(obj, "SignalType", ""),
        "CadModelPath": getattr(obj, "CadModelPath", ""),
        "CadModelFormat": getattr(obj, "CadModelFormat", ""),
        "CadModelSha256": getattr(obj, "CadModelSha256", ""),
    }


def _project_object(document) -> object | None:
    for obj in getattr(document, "Objects", []) or []:
        if hasattr(obj, "ProjectId") and hasattr(obj, "PlcMake") and hasattr(obj, "PlcLine"):
            return obj
    return None


def _step_cad_ref(part):
    for cad_ref in part.cad_refs:
        if cad_ref.format.upper() == "STEP":
            return cad_ref
    return part.cad_refs[0] if part.cad_refs else None


def starter_layout_specs_for_project(project: object | None) -> tuple[LayoutObjectSpec, ...]:
    specs = _starter_layout_specs_with_panel_catalog()
    if project is None:
        return specs
    catalog = load_hardware_catalog(default_catalog_path())
    line = line_catalog(
        catalog,
        str(getattr(project, "PlcMake", "")),
        str(getattr(project, "PlcLine", "")),
    )
    if line is None:
        return specs
    cpu = part_by_name(line.cpus, str(getattr(project, "PlcCPU", "")))
    if cpu is None:
        return specs
    cad_ref = _step_cad_ref(cpu)
    updated_specs = []
    for spec in specs:
        if spec.name != "CE_PLC_Rack":
            updated_specs.append(spec)
            continue
        updated_specs.append(
            replace(
                spec,
                manufacturer=str(getattr(project, "PlcMake", "")) or line.make,
                part_number=cpu.part_number,
                description=f"{cpu.name} PLC CPU placeholder",
                channel_count=cpu.di + cpu.do + cpu.ai + cpu.ao,
                cad_model_path=cad_ref.local_path if cad_ref else "",
                cad_model_format=cad_ref.format if cad_ref else "",
                cad_model_sha256=cad_ref.sha256 if cad_ref else "",
            )
        )
    return tuple(updated_specs)


def _starter_layout_specs_with_panel_catalog() -> tuple[LayoutObjectSpec, ...]:
    catalog = load_panel_hardware_catalog(default_panel_catalog_path())
    updated_specs = []
    for spec in STARTER_LAYOUT_SPECS:
        part = part_for_layout(catalog, spec.name)
        if part is None:
            updated_specs.append(spec)
            continue
        updated_specs.append(
            replace(
                spec,
                manufacturer=part.manufacturer,
                part_number=part.part_number,
                description=part.description,
            )
        )
    return tuple(updated_specs)


def create_layout_object(document, spec: LayoutObjectSpec):
    obj = document.addObject("Part::FeaturePython", spec.name)
    ControlsLayoutObject(obj, spec.role)
    return apply_layout_spec(obj, spec)


def create_starter_layout_objects(document=None) -> list[object]:
    if document is None:
        document = App.ActiveDocument
    project = _project_object(document)
    specs = starter_layout_specs_for_project(project)
    objects = [create_layout_object(document, spec) for spec in specs]
    if project is not None and (hasattr(project, "addProperty") or hasattr(project, "ElectricalDevices")):
        from controls_wb.model.electrical import register_electrical_device

        for obj in objects:
            if obj.CERole in {CERoles.PLC_CONTROLLER, CERoles.TERMINAL_STRIP}:
                register_electrical_device(project, obj)
    return objects


def _add_property(obj, property_type: str, name: str, group: str, description: str) -> None:
    if name not in set(getattr(obj, "PropertiesList", []) or []):
        obj.addProperty(property_type, name, group, description)


def _object_for_identity(document, identity: str):
    """Find the one document object carrying ``identity``, if it exists."""
    for obj in getattr(document, "Objects", []) or []:
        if getattr(obj, "CEIdentity", "") == identity:
            return obj
    return None


def _allocation_identity(project, kind: str, key: str) -> str:
    """Derive a repeatable occurrence identity from project and PLC coordinates."""
    project_key = str(getattr(project, "CEIdentity", "") or getattr(project, "ProjectId", "")).strip()
    if not project_key:
        raise ValueError("PLC allocation occurrences require a project identity or ProjectId.")
    return imported_ce_identity("ceproject.plc-allocation", f"{project_key}:{kind}:{key}")


def _materialize_allocation_object(document, name: str, role: str, identity: str):
    """Create or reuse a typed allocation occurrence without duplicating it."""
    existing = _object_for_identity(document, identity)
    if existing is not None:
        if getattr(existing, "CERole", "") != role:
            raise ValueError(f"Allocation identity {identity} belongs to {getattr(existing, 'CERole', '')!r}.")
        return existing
    obj = document.addObject("App::FeaturePython", name)
    ControlsLayoutObject(obj, role)
    # The object was created with a random identity; replace it before it has
    # any externally visible relationship so allocation occurrences are stable
    # across reruns and save/reopen cycles.
    obj.CEIdentity = identity
    return obj


def _signal_and_paths_for_allocation(project, signal_tag: str):
    """Return the typed signal and paths carrying one allocated I/O tag.

    Allocation records predate typed path materialization, so the mutable tag is
    used only to discover the existing logical signal.  The persisted channel
    relationship itself is an object link (and therefore carries CE identity),
    never a second tag-derived identity.
    """

    matches = [
        signal
        for signal in (getattr(project, "ElectricalSignals", []) or [])
        if getattr(signal, "CERole", "") == CERoles.SIGNAL
        and str(getattr(signal, "SignalTag", "") or "") == signal_tag
    ]
    if len(matches) > 1:
        raise ValueError(f"Allocated signal tag {signal_tag!r} resolves to multiple typed signals.")
    typed_signal = matches[0] if matches else None
    paths = [
        path
        for path in (getattr(project, "ElectricalPaths", []) or [])
        if typed_signal is not None and getattr(path, "SignalObject", None) is typed_signal
    ]
    return typed_signal, paths


def _materialize_allocation_signal(document, project, signal_tag: str):
    """Create or reuse the one typed signal represented by an allocated tag."""

    typed_signal, _ = _signal_and_paths_for_allocation(project, signal_tag)
    if typed_signal is not None:
        return typed_signal
    from controls_wb.model.electrical import ElectricalSignalObject

    identity = _allocation_identity(project, "signal", signal_tag)
    existing = _object_for_identity(document, identity)
    if existing is not None:
        if getattr(existing, "CERole", "") != CERoles.SIGNAL:
            raise ValueError(f"Allocation signal identity {identity} belongs to a non-signal object.")
        typed_signal = existing
    else:
        typed_signal = document.addObject("App::FeaturePython", "CE_Signal")
        ElectricalSignalObject(typed_signal, identity)
    _add_property(typed_signal, "App::PropertyString", "SignalTag", "Electrical Signal", "Signal tag")
    _add_property(typed_signal, "App::PropertyLinkList", "ConnectionPaths", "Electrical Signal", "Paths carrying this signal")
    if str(getattr(typed_signal, "SignalTag", "") or "") not in {"", signal_tag}:
        raise ValueError(f"Allocation signal {identity} has a conflicting tag.")
    typed_signal.SignalTag = signal_tag
    _add_property(project, "App::PropertyLinkList", "ElectricalSignals", "Electrical Graph", "Typed signal objects owned by this project")
    existing_signals = list(getattr(project, "ElectricalSignals", []) or [])
    if typed_signal not in existing_signals:
        project.ElectricalSignals = existing_signals + [typed_signal]
    return typed_signal


def materialize_plc_allocation(document, project: object | None = None) -> dict[str, object]:
    """Materialize a persisted project's PLC rack, modules, and channels.

    Each occurrence has a deterministic CE identity derived from the project
    and allocation coordinates.  Re-running is idempotent and preserves the
    object links that make the catalog allocation navigable in FreeCAD.
    """

    project = project or _project_object(document)
    if project is None:
        raise ValueError("PLC allocation materialization requires one CE_Project.")
    from controls_wb.io_list import explicit_io_signals_from_project, persist_io_allocation_to_project
    from controls_wb.model.electrical import register_electrical_device

    allocation = persist_io_allocation_to_project(project)
    signals = explicit_io_signals_from_project(project)
    rack_values = {module.rack for module in allocation.modules}
    if len(rack_values) != 1:
        raise ValueError("PLC allocation must contain exactly one rack to materialize it.")
    rack_number = next(iter(rack_values))
    rack_identity = _allocation_identity(project, "rack", rack_number)
    rack = _materialize_allocation_object(document, "CE_PLC_Allocation_Rack", CERoles.PLC_RACK, rack_identity)
    for property_type, name, description in (
        ("App::PropertyString", "RackNumber", "PLC rack number"),
        ("App::PropertyLinkList", "Modules", "Materialized PLC modules"),
    ):
        _add_property(rack, property_type, name, "PLC Allocation", description)
    rack.RackNumber = rack_number

    modules = []
    channels = []
    for module in allocation.modules:
        module_identity = _allocation_identity(project, "module", f"{module.rack}:{module.slot}")
        module_obj = _materialize_allocation_object(document, "CE_PLC_Module", CERoles.PLC_MODULE, module_identity)
        for property_type, name, description in (
            ("App::PropertyLink", "RackObject", "Owning PLC rack"),
            ("App::PropertyString", "RackNumber", "PLC rack number"),
            # ControlsLayoutObject already supplies SlotNumber as an integer.
            # Keep that native property type for materialized occurrences: PLC
            # allocation records deserialize coordinates as strings, while
            # FreeCAD rejects assigning those strings to App::PropertyInteger.
            ("App::PropertyInteger", "SlotNumber", "PLC slot number"),
            ("App::PropertyString", "ModuleName", "Catalog module name"),
            ("App::PropertyString", "PartNumber", "Catalog part number"),
            ("App::PropertyString", "CatalogSourceId", "Hardware catalog source"),
            ("App::PropertyBool", "IsCPU", "Whether this module is the selected CPU"),
            ("App::PropertyLinkList", "Channels", "Materialized allocated channels"),
        ):
            _add_property(module_obj, property_type, name, "PLC Allocation", description)
        module_obj.RackObject = rack
        module_obj.RackNumber = module.rack
        module_obj.SlotNumber = int(module.slot)
        module_obj.ModuleName = module.module_name
        module_obj.PartNumber = module.part_number
        module_obj.CatalogSourceId = module.source_id
        module_obj.IsCPU = module.is_cpu
        modules.append(module_obj)
        register_electrical_device(project, module_obj)

        module_channels = []
        for signal in signals:
            if signal.rack != module.rack or signal.slot != module.slot:
                continue
            channel_identity = _allocation_identity(project, "channel", f"{signal.rack}:{signal.slot}:{signal.signal_type}:{signal.channel}")
            channel_obj = _materialize_allocation_object(document, "CE_PLC_Channel", CERoles.PLC_CHANNEL, channel_identity)
            for property_type, name, description in (
                ("App::PropertyLink", "ModuleObject", "Owning PLC module"),
                ("App::PropertyString", "RackNumber", "PLC rack number"),
                ("App::PropertyInteger", "SlotNumber", "PLC slot number"),
                ("App::PropertyString", "ChannelNumber", "PLC channel number"),
                ("App::PropertyString", "SignalType", "Allocated I/O signal type"),
                ("App::PropertyString", "AllocatedSignalTag", "Allocated logical I/O signal tag"),
                ("App::PropertyString", "SignalAddress", "Allocated logical I/O address"),
                ("App::PropertyLink", "AllocatedSignalObject", "Typed electrical signal allocated to this channel"),
                ("App::PropertyLinkList", "ElectricalPaths", "Typed electrical paths carrying the allocated signal"),
            ):
                _add_property(channel_obj, property_type, name, "PLC Allocation", description)
            channel_obj.ModuleObject = module_obj
            channel_obj.RackNumber = signal.rack
            channel_obj.SlotNumber = int(signal.slot)
            channel_obj.ChannelNumber = signal.channel
            channel_obj.SignalType = signal.signal_type
            channel_obj.AllocatedSignalTag = signal.tag
            channel_obj.SignalAddress = signal.address
            typed_signal = _materialize_allocation_signal(document, project, signal.tag)
            _add_property(typed_signal, "App::PropertyLink", "AllocatedChannelObject", "Electrical Signal", "Allocated PLC channel carrying this signal")
            previous_channel = getattr(typed_signal, "AllocatedChannelObject", None)
            if previous_channel is not None and previous_channel is not channel_obj:
                if getattr(previous_channel, "SignalType", "") != signal.signal_type:
                    raise ValueError(f"Typed signal {signal.tag} cannot migrate across PLC signal types.")
                # A coordinate-derived channel is a new physical occurrence,
                # but the logical typed signal and its downstream design data
                # survive a same-type move.  Rewrite only the PLC endpoint;
                # path/wire/terminal/signal identities remain immutable.
                for path in list(getattr(previous_channel, "ElectricalPaths", []) or []):
                    terminals = list(getattr(path, "TerminalObjects", []) or [])
                    if not terminals:
                        raise ValueError(f"PLC channel move cannot migrate path {getattr(path, 'CEIdentity', '')} without terminals.")
                    first_terminal = terminals[0]
                    if getattr(first_terminal, "OwnerIdentity", "") != getattr(previous_channel, "CEIdentity", ""):
                        raise ValueError(f"PLC channel move found path {getattr(path, 'CEIdentity', '')} owned by another channel.")
                    first_terminal.OwnerIdentity = channel_obj.CEIdentity
                    first_terminal.Designation = signal.address
                previous_channel.ElectricalPaths = []
            typed_signal.AllocatedChannelObject = channel_obj
            _, paths = _signal_and_paths_for_allocation(project, signal.tag)
            channel_obj.AllocatedSignalObject = typed_signal
            channel_obj.ElectricalPaths = paths
            register_electrical_device(project, channel_obj)
            module_channels.append(channel_obj)
            channels.append(channel_obj)
        module_obj.Channels = module_channels
    rack.Modules = modules
    register_electrical_device(project, rack)
    _prune_unlinked_allocation_occurrences(document, project, {obj.CEIdentity for obj in (rack, *modules, *channels)})
    return {"rack": rack, "modules": tuple(modules), "channels": tuple(channels)}


def _prune_unlinked_allocation_occurrences(document, project, desired_identities: set[str]) -> None:
    """Remove only stale allocation occurrences without downstream path data."""

    stale = [
        obj for obj in list(getattr(document, "Objects", []) or [])
        if getattr(obj, "CERole", "") in {CERoles.PLC_RACK, CERoles.PLC_MODULE, CERoles.PLC_CHANNEL}
        and getattr(obj, "CEIdentity", "") not in desired_identities
    ]
    for obj in stale:
        if getattr(obj, "CERole", "") == CERoles.PLC_CHANNEL and getattr(obj, "ElectricalPaths", []):
            raise ValueError(f"Cannot remove stale PLC channel {getattr(obj, 'CEIdentity', '')} while it owns electrical paths.")
    if not stale:
        return
    stale_set = set(stale)
    retired_signals = []
    for obj in stale:
        if getattr(obj, "CERole", "") != CERoles.PLC_CHANNEL:
            continue
        signal = getattr(obj, "AllocatedSignalObject", None)
        if signal is not None and getattr(signal, "AllocatedChannelObject", None) is obj:
            signal.AllocatedChannelObject = None
            if not getattr(signal, "ConnectionPaths", []) and signal not in retired_signals:
                retired_signals.append(signal)
    stale_set.update(retired_signals)
    for owner, property_name in ((project, "ElectricalDevices"),):
        if hasattr(owner, property_name):
            setattr(owner, property_name, [item for item in getattr(owner, property_name, []) or [] if item not in stale_set])
    if hasattr(project, "ElectricalSignals"):
        project.ElectricalSignals = [item for item in getattr(project, "ElectricalSignals", []) or [] if item not in stale_set]
    remove = getattr(document, "removeObject", None)
    for obj in stale:
        if callable(remove):
            remove(getattr(obj, "Name", ""))
        elif hasattr(document, "Objects"):
            document.Objects.remove(obj)


def allocation_electrical_graph_findings(project, objects) -> tuple[tuple[str, str, str], ...]:
    """Validate persisted PLC-channel links to the typed electrical graph.

    This deliberately checks FreeCAD links as well as cached tags so copied,
    stale, or manually edited occurrence objects cannot silently claim a valid
    channel-to-path relationship.
    """

    findings = []
    for channel in objects:
        if getattr(channel, "CERole", "") != CERoles.PLC_CHANNEL:
            continue
        tag = str(getattr(channel, "AllocatedSignalTag", "") or "")
        channel_id = str(getattr(channel, "CEIdentity", "") or getattr(channel, "Name", "PLC channel"))
        signal = getattr(channel, "AllocatedSignalObject", None)
        if signal is None:
            findings.append(("ERROR", "allocated_channel_missing_signal", f"PLC channel {channel_id} has no typed signal link for {tag}."))
            continue
        if signal not in (getattr(project, "ElectricalSignals", []) or []):
            findings.append(("ERROR", "allocated_channel_unregistered_signal", f"PLC channel {channel_id} links to a signal not registered on the project."))
        if getattr(signal, "CERole", "") != CERoles.SIGNAL:
            findings.append(("ERROR", "allocated_channel_wrong_role_signal", f"PLC channel {channel_id} links to a non-signal object."))
            continue
        if str(getattr(signal, "SignalTag", "") or "") != tag:
            findings.append(("ERROR", "allocated_channel_signal_tag_mismatch", f"PLC channel {channel_id} signal link does not match allocated tag {tag}."))
        if getattr(signal, "AllocatedChannelObject", None) is not channel:
            findings.append(("ERROR", "allocated_channel_reverse_link_missing", f"PLC channel {channel_id} is not the signal's reciprocal allocated channel."))
        linked_paths = list(getattr(channel, "ElectricalPaths", []) or [])
        for path in (getattr(project, "ElectricalPaths", []) or []):
            if getattr(path, "SignalObject", None) is signal and path not in linked_paths:
                findings.append(("ERROR", "allocated_channel_path_link_missing", f"PLC channel {channel_id} is missing a link to consuming path {getattr(path, 'CEIdentity', '')}."))
        for path in linked_paths:
            if getattr(path, "CERole", "") != CERoles.CONNECTION_PATH:
                findings.append(("ERROR", "allocated_channel_wrong_role_path", f"PLC channel {channel_id} links to a non-path object."))
            elif getattr(path, "SignalObject", None) is not signal:
                findings.append(("ERROR", "allocated_channel_path_signal_mismatch", f"PLC channel {channel_id} path does not carry its typed signal."))
            else:
                terminals = list(getattr(path, "TerminalObjects", []) or [])
                first_terminal = terminals[0] if terminals else None
                if first_terminal is None or getattr(first_terminal, "CERole", "") != CERoles.PLC_CHANNEL_TERMINAL:
                    findings.append(("ERROR", "allocated_channel_path_terminal_missing", f"PLC channel {channel_id} path has no PLC channel terminal."))
                elif getattr(first_terminal, "OwnerIdentity", "") != getattr(channel, "CEIdentity", ""):
                    findings.append(("ERROR", "allocated_channel_path_owner_mismatch", f"PLC channel {channel_id} does not own its path PLC terminal."))
                elif getattr(first_terminal, "Designation", "") != getattr(channel, "SignalAddress", ""):
                    findings.append(("ERROR", "allocated_channel_path_address_mismatch", f"PLC channel {channel_id} path terminal does not match allocated address {getattr(channel, 'SignalAddress', '')}."))
    return tuple(sorted(findings, key=lambda finding: (finding[0], finding[1], finding[2])))


class ControlsLayoutObject:
    def __init__(self, obj, role: str):
        obj.Proxy = self
        self.Type = "ControlsLayoutObject"
        self.Role = role
        ensure_layout_properties(obj)
        ensure_object_identity(obj, role)

    def execute(self, obj):
        if Part is not None:
            obj.Shape = Part.makeBox(obj.Width, obj.Depth, obj.Height)

    def onDocumentRestored(self, obj):
        ensure_layout_properties(obj)
        role = getattr(self, "Role", "") or role_for_layout_name(getattr(obj, "Name", ""))
        self.Role = role
        ensure_object_identity(obj, role)

    def __getstate__(self):
        return {"Type": self.Type, "Role": self.Role}

    def __setstate__(self, state):
        self.Type = state.get("Type", "ControlsLayoutObject")
        self.Role = state.get("Role", "")


def role_for_layout_name(name: str) -> str:
    for spec in STARTER_LAYOUT_SPECS:
        if spec.name == name:
            return spec.role
    raise ValueError(f"Cannot restore CEProject role for layout object: {name}")
