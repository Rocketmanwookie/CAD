from __future__ import annotations

import argparse
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from qet_tb_generator.model import Terminal, TerminalBlock, VALID_SIDES, VALID_TERMINAL_TYPES
from qet_tb_generator.qet_xml import block_from_xml, write_block


class TerminalBlockApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("QET Terminal Block Generator")
        self.block_name = tk.StringVar(value="TB1")
        self.tag = tk.StringVar(value="X1:1")
        self.label = tk.StringVar(value="24VDC")
        self.side = tk.StringVar(value="left")
        self.terminal_type = tk.StringVar(value="feedthrough")
        self.bridge = tk.StringVar()
        self.wire = tk.StringVar()
        self.terminals: list[Terminal] = []
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        form = ttk.Frame(frame)
        form.grid(row=0, column=0, sticky="ew")
        for column in range(6):
            form.columnconfigure(column, weight=1)

        ttk.Label(form, text="Block").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.block_name, width=12).grid(row=1, column=0, sticky="ew")
        ttk.Label(form, text="Tag").grid(row=0, column=1, sticky="w")
        ttk.Entry(form, textvariable=self.tag, width=12).grid(row=1, column=1, sticky="ew")
        ttk.Label(form, text="Label").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.label, width=20).grid(row=1, column=2, sticky="ew")
        ttk.Label(form, text="Side").grid(row=0, column=3, sticky="w")
        ttk.Combobox(form, textvariable=self.side, values=sorted(VALID_SIDES), state="readonly", width=8).grid(row=1, column=3, sticky="ew")
        ttk.Label(form, text="Type").grid(row=0, column=4, sticky="w")
        ttk.Combobox(form, textvariable=self.terminal_type, values=sorted(VALID_TERMINAL_TYPES), state="readonly", width=12).grid(row=1, column=4, sticky="ew")
        ttk.Button(form, text="Add", command=self.add_terminal).grid(row=1, column=5, sticky="ew")

        extra = ttk.Frame(frame)
        extra.grid(row=1, column=0, sticky="ew", pady=(8, 8))
        extra.columnconfigure(1, weight=1)
        extra.columnconfigure(3, weight=1)
        ttk.Label(extra, text="Bridge").grid(row=0, column=0, sticky="w")
        ttk.Entry(extra, textvariable=self.bridge).grid(row=0, column=1, sticky="ew")
        ttk.Label(extra, text="Wire").grid(row=0, column=2, sticky="w", padx=(8, 0))
        ttk.Entry(extra, textvariable=self.wire).grid(row=0, column=3, sticky="ew")

        columns = ("tag", "label", "side", "type", "bridge", "wire")
        self.table = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        for column in columns:
            self.table.heading(column, text=column.title())
            self.table.column(column, width=120, anchor="w")
        self.table.grid(row=2, column=0, sticky="nsew")
        frame.rowconfigure(2, weight=1)

        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(buttons, text="Import XML", command=self.import_xml).pack(side="left")
        ttk.Button(buttons, text="Export XML", command=self.export_xml).pack(side="left", padx=(8, 0))
        ttk.Button(buttons, text="Remove Selected", command=self.remove_selected).pack(side="right")

    def current_block(self) -> TerminalBlock:
        return TerminalBlock(name=self.block_name.get(), terminals=list(self.terminals))

    def add_terminal(self) -> None:
        try:
            terminal = Terminal(
                tag=self.tag.get(),
                label=self.label.get(),
                side=self.side.get(),
                terminal_type=self.terminal_type.get(),
                bridge=self.bridge.get(),
                wire=self.wire.get(),
            )
        except ValueError as exc:
            messagebox.showerror("Invalid terminal", str(exc))
            return

        self.terminals.append(terminal)
        self._append_table_row(terminal)
        self.tag.set(self.current_block().next_tag())
        self.label.set("")
        self.bridge.set("")
        self.wire.set("")

    def _append_table_row(self, terminal: Terminal) -> None:
        self.table.insert(
            "",
            "end",
            values=(
                terminal.tag,
                terminal.label,
                terminal.side,
                terminal.terminal_type,
                terminal.bridge,
                terminal.wire,
            ),
        )

    def remove_selected(self) -> None:
        selected = list(self.table.selection())
        if not selected:
            return
        indexes = sorted((self.table.index(item) for item in selected), reverse=True)
        for item in selected:
            self.table.delete(item)
        for index in indexes:
            del self.terminals[index]

    def export_xml(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Export terminal block XML",
            defaultextension=".xml",
            filetypes=(("XML files", "*.xml"), ("All files", "*.*")),
        )
        if not path:
            return
        try:
            write_block(path, self.current_block())
        except ValueError as exc:
            messagebox.showerror("Export failed", str(exc))
            return
        messagebox.showinfo("Export complete", f"Wrote {Path(path).name}")

    def import_xml(self) -> None:
        path = filedialog.askopenfilename(
            title="Import terminal block XML",
            filetypes=(("XML files", "*.xml"), ("All files", "*.*")),
        )
        if not path:
            return
        try:
            block = block_from_xml(Path(path).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            messagebox.showerror("Import failed", str(exc))
            return
        self.block_name.set(block.name)
        self.terminals = list(block.terminals)
        for item in self.table.get_children():
            self.table.delete(item)
        for terminal in self.terminals:
            self._append_table_row(terminal)
        self.tag.set(self.current_block().next_tag())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="QElectroTech terminal block generator")
    parser.add_argument("--version", action="store_true", help="print version and exit")
    args = parser.parse_args(argv)
    if args.version:
        from qet_tb_generator import __version__

        print(__version__)
        return 0

    root = tk.Tk()
    TerminalBlockApp(root)
    root.mainloop()
    return 0
