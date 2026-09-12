# SPDX-License-Identifier: MIT
"""Small, testable transaction boundary for FreeCAD document mutations."""

from contextlib import contextmanager


@contextmanager
def document_transaction(document, label: str):
    """Commit a document operation atomically when FreeCAD supports transactions."""

    open_transaction = getattr(document, "openTransaction", None)
    commit_transaction = getattr(document, "commitTransaction", None)
    abort_transaction = getattr(document, "abortTransaction", None)
    started = callable(open_transaction)

    if started:
        open_transaction(label)
    try:
        yield
    except Exception:
        if started and callable(abort_transaction):
            abort_transaction()
        raise
    else:
        if started and callable(commit_transaction):
            commit_transaction()
