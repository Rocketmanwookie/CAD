# SPDX-License-Identifier: MIT
"""Extract deterministic wire routes from selected FreeCAD geometry."""

from __future__ import annotations

from controls_wb.electrical_path import RoutePoint
from controls_wb.identity import CERoles


def selected_wire_and_route_points(selection_ex):
    """Return one selected CE wire and its ordered route points.

    A route is captured from the vertices of selected geometry other than the
    CE_Wire itself.  The helper intentionally uses only the small SelectionEx
    surface so it can be verified with lightweight fakes outside FreeCAD.
    """

    selected_wires = [
        entry.Object
        for entry in selection_ex
        if getattr(entry.Object, "CERole", "") == CERoles.WIRE
    ]
    if len(selected_wires) != 1:
        raise ValueError("Select exactly one typed CE_Wire and route geometry.")

    wire = selected_wires[0]
    points: list[RoutePoint] = []
    for entry in selection_ex:
        if entry.Object is wire:
            continue
        subobjects = list(getattr(entry, "SubObjects", []) or [])
        candidates = subobjects or [getattr(entry, "Object", None)]
        for candidate in candidates:
            vertices = list(getattr(candidate, "Vertexes", []) or [])
            for vertex in vertices:
                point = getattr(vertex, "Point", vertex)
                route_point = RoutePoint(float(point.x), float(point.y), float(point.z))
                if not points or route_point != points[-1]:
                    points.append(route_point)

    if len(points) < 2:
        raise ValueError("Select route geometry with at least two distinct vertices.")
    return wire, tuple(points)
