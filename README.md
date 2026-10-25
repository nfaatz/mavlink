# sysml-icd

Generate interface control documents (ICDs) and protocol definitions from SysML v2 models.
First target: MAVLink. The SysML model must produce the same wire format as the official
MAVLink XML (verified via CRC_EXTRA).

## Setup
```
python -m venv .venv
.venv\Scripts\activate          # Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
git submodule update --init
```

## Run
```
python -m pytest -v                     # all tests
python scripts/generate_enums.py        # regenerate models/generated/ from fixtures/mini.xml
```

## Layout
```
src/sysml_icd/sysml/     SysML parser (protocol-agnostic)
src/sysml_icd/mavlink/   MAVLink rules: wire order, CRC, XML import/export, SysML extraction
scripts/                 one-off helpers and exploration
models/                  hand-written SysML models
models/generated/        generated SysML, do not edit
fixtures/                reference input (excerpt of MAVLink XML)
tests/                   pytest tests
docs/adr/                architecture decision records
reference/mavlink/       official MAVLink repo (git submodule, read-only)
```

## References
- MAVLink definitions: https://github.com/mavlink/mavlink/tree/master/message_definitions/v1.0
- Serialization and CRC_EXTRA: https://mavlink.io/en/guide/serialization.html
