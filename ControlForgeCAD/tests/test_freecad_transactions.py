# SPDX-License-Identifier: MIT

import pytest

from controls_wb.freecad_transactions import document_transaction


class FakeDocument:
    def __init__(self):
        self.events = []

    def openTransaction(self, label):
        self.events.append(("open", label))

    def commitTransaction(self):
        self.events.append(("commit", None))

    def abortTransaction(self):
        self.events.append(("abort", None))


def test_document_transaction_commits_successful_mutation():
    document = FakeDocument()

    with document_transaction(document, "Create controls project"):
        document.events.append(("mutate", None))

    assert document.events == [
        ("open", "Create controls project"),
        ("mutate", None),
        ("commit", None),
    ]


def test_document_transaction_aborts_failed_mutation():
    document = FakeDocument()

    with pytest.raises(ValueError, match="invalid"):
        with document_transaction(document, "Add I/O signal"):
            raise ValueError("invalid")

    assert document.events == [("open", "Add I/O signal"), ("abort", None)]


def test_document_transaction_is_safe_for_lightweight_test_documents():
    with document_transaction(object(), "No-op"):
        pass
