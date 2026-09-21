# SPDX-License-Identifier: MIT

import json

import pytest

from controls_wb.electrical_path import RoutePoint
from controls_wb.identity import CERoles
from controls_wb.model.electrical import update_wire_route_object
from controls_wb.route_capture import selected_wire_and_route_points


class Point:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z


class Vertex:
    def __init__(self, x, y, z):
        self.Point = Point(x, y, z)


class Geometry:
    def __init__(self, *vertices):
        self.Vertexes = [Vertex(*vertex) for vertex in vertices]


class Selection:
    def __init__(self, obj, *subobjects):
        self.Object = obj
        self.SubObjects = subobjects


class Wire:
    CERole = CERoles.WIRE
    CEIdentity = "urn:uuid:11111111-1111-4111-8111-111111111111"
    FromTerminalIdentity = "urn:uuid:22222222-2222-4222-8222-222222222222"
    ToTerminalIdentity = "urn:uuid:33333333-3333-4333-8333-333333333333"
    WireTag = "W-101"
    ConductorSize = "18 AWG"
    Color = "BK"
    CircuitFunction = "DI"
    ConduitIdentity = "ce-conduit-1"
    HasSpecifiedLength = False
    SpecifiedLength = "0 mm"
    RoutePoints = []
    CalculatedLength = "0 mm"
    Proxy = None


def test_capture_requires_one_wire_and_deduplicates_joined_vertices():
    wire = Wire()
    captured_wire, points = selected_wire_and_route_points([
        Selection(wire),
        Selection(object(), Geometry((0, 0, 0), (100, 0, 0))),
        Selection(object(), Geometry((100, 0, 0), (100, 50, 0))),
    ])
    assert captured_wire is wire
    assert points == (RoutePoint(0, 0, 0), RoutePoint(100, 0, 0), RoutePoint(100, 50, 0))


def test_capture_rejects_missing_wire_or_insufficient_geometry():
    with pytest.raises(ValueError, match="exactly one"):
        selected_wire_and_route_points([])
    with pytest.raises(ValueError, match="at least two"):
        selected_wire_and_route_points([Selection(Wire()), Selection(object(), Geometry((0, 0, 0)))])


def test_route_update_preserves_identity_and_calculates_length():
    wire = Wire()
    result = update_wire_route_object(wire, (RoutePoint(0, 0, 0), RoutePoint(30, 40, 0)))
    assert result is wire
    assert wire.CEIdentity == "urn:uuid:11111111-1111-4111-8111-111111111111"
    assert wire.CalculatedLength == "50.0 mm"
    assert json.loads(wire.RoutePoints[0])["sequence"] == 0
