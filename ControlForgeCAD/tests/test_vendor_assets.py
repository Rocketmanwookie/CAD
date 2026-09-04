# SPDX-License-Identifier: MIT

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
