# SPDX-License-Identifier: MIT

from dataclasses import replace

import pytest

from controls_wb.hardware_catalog import default_catalog_path, load_hardware_catalog
from controls_wb.vendor_assets import selected_siemens_asset_requests, vendor_asset_manifest_json, vendor_part_numbers_csv


def test_selected_siemens_assets_are_review_gated_and_source_backed():
    catalog = load_hardware_catalog(default_catalog_path())
    requests = selected_siemens_asset_requests(
        catalog, "S7-1200", "CPU 1212C DC/DC/DC", ("SM 1221 DI 16x24 V DC",)
    )
    assert [request.part_number for request in requests] == ["6ES7212-1AE40-0XB0", "6ES7221-1BH32-0XB0"]
    assert all(request.acquisition_status == "manual_review_required" for request in requests)
    assert all(request.source_url.startswith("https://") for request in requests)
    assert '"requested_formats": [' in vendor_asset_manifest_json(requests)
    assert vendor_part_numbers_csv(requests) == (
        "Manufacturer,PartNumber,Quantity\n"
        "Siemens,6ES7212-1AE40-0XB0,1\n"
        "Siemens,6ES7221-1BH32-0XB0,1\n"
    )


@pytest.mark.parametrize("line,cpu,modules,message", [
    ("unknown", "CPU 1212C DC/DC/DC", (), "product line"),
    ("S7-1200", "unknown", (), "CPU selection"),
    ("S7-1200", "CPU 1212C DC/DC/DC", ("missing module",), "module selection"),
])
def test_unknown_selections_cannot_silently_produce_partial_manifest(line, cpu, modules, message):
    with pytest.raises(ValueError, match=message):
        selected_siemens_asset_requests(load_hardware_catalog(), line, cpu, modules)


def test_csv_aggregates_duplicates_and_rejects_incomplete_rows():
    request = selected_siemens_asset_requests(load_hardware_catalog(), "S7-1200", "CPU 1212C DC/DC/DC")[0]
    padded = replace(request, manufacturer=" Siemens ", part_number=" " + request.part_number + " ")
    assert vendor_part_numbers_csv([request, padded]).endswith("Siemens,6ES7212-1AE40-0XB0,2\n")
    for invalid in (replace(request, manufacturer=" "), replace(request, part_number="")):
        with pytest.raises(ValueError, match="Missing manufacturer or part number"):
            vendor_part_numbers_csv([request, invalid])


def test_catalog_part_without_order_number_fails():
    catalog = load_hardware_catalog()
    line = catalog.lines[0]
    bad_cpu = replace(line.cpus[0], part_number=" ")
    catalog = replace(catalog, lines=(replace(line, cpus=(bad_cpu,)),))
    with pytest.raises(ValueError, match="Missing manufacturer part number"):
        selected_siemens_asset_requests(catalog, line.line, bad_cpu.name)


def test_seed_cad_references_do_not_claim_exact_part_verification():
    catalog = load_hardware_catalog()
    for cpu in catalog.lines[0].cpus:
        request = selected_siemens_asset_requests(catalog, "S7-1200", cpu.name)[0]
        assert request.cad_match_status == "unverified"
        assert '"cad_match_status": "unverified"' in vendor_asset_manifest_json([request])


def test_cli_outputs_no_partial_csv_on_unknown_module(capsys):
    from controls_wb.vendor_assets import main
    assert main(["--cpu", "CPU 1212C DC/DC/DC", "--module", "unknown"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "unknown" in captured.err


def test_cli_part_numbers_only_are_unique(capsys):
    from controls_wb.vendor_assets import main
    assert main(["--cpu", "CPU 1212C DC/DC/DC", "--module", "SM 1221 DI 16x24 V DC",
                 "--module", "SM 1221 DI 16x24 V DC", "--format", "part-numbers"]) == 0
    assert capsys.readouterr().out == "6ES7212-1AE40-0XB0\n6ES7221-1BH32-0XB0\n"


def test_manifest_rejects_excess_and_unknown_module_limits():
    catalog = load_hardware_catalog()
    module = "SM 1221 DI 16x24 V DC"
    with pytest.raises(ValueError, match="exceed CPU limit 2"):
        selected_siemens_asset_requests(catalog, "S7-1200", "CPU 1212C DC/DC/DC", (module,) * 3)
    with pytest.raises(ValueError, match="limit is unknown"):
        selected_siemens_asset_requests(catalog, "S7-1200", "CPU 1214C DC/DC/DC", (module,))
