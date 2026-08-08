# QElectroTech Terminal Block Generator

Licensed under the General Public License 2.0.

This is an original starter project for a terminal block generator helper for
QElectroTech. It is intentionally small: the domain logic is pure Python, the
GUI is Tkinter, and exported data is XML so later QElectroTech integration can
adapt the output without rewriting the model.

## Directory Contents

- `src/qet_tb_generator`: source code
- `sample_projects`: small XML files for smoke testing
- `tests`: pure-Python tests
- `run.py`: local launcher for the GUI

## Install For Development

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Tkinter must be available on Linux:

```bash
sudo apt-get install python3-tk
```

## Run

```bash
python run.py
```

or, after installation:

```bash
qet_tb_generator
```

## Test

```bash
python3 -m pytest
python3 -m compileall src
```

## XML Format

The first XML format is a compact terminal block interchange file:

```xml
<terminal_block_project generator="qet_tb_generator" schema_version="0.1">
  <terminal_block name="TB1">
    <terminal index="1" tag="X1:1" label="24VDC" side="left" type="feedthrough" bridge="" wire=""/>
  </terminal_block>
</terminal_block_project>
```

This is not yet a full QElectroTech `.qet` project writer. The next integration
step is mapping these terminal rows into the exact QElectroTech project/plugin
contract used by the installed QET version.
