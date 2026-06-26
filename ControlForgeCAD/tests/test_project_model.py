# SPDX-License-Identifier: MIT

import json

from controls_wb.intake import default_project_intake
from controls_wb.model.project import _project_payloads


def test_project_payloads_include_contacts_sources_and_questions():
    contacts, sources, questions = _project_payloads(default_project_intake())

    contact_records = [json.loads(contact) for contact in contacts]
    source_records = [json.loads(source) for source in sources]
    question_records = [json.loads(question) for question in questions]

    assert any(record["role"] == "Controls lead" for record in contact_records)
    assert any(record["type"] == "manual_entry" and "project.name" in record["fieldIds"] for record in source_records)
    assert any(record["fieldId"] == "controls.plcPlatform" and record["ask"] == "Controls lead" for record in question_records)
