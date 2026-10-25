# ADR 0001: Own parser for a SysML v2 subset

Status: accepted (temporary)

## Context
Python generators need to read SysML v2 models. Options:
- Syside Automator: proprietary, paid license, vendor is a potential competitor.
- SysML v2 Pilot Implementation (JSON export): complete and official, but heavy setup (Java, Jupyter).
- Own parser: fast to build, limited to the constructs this project uses.

## Decision
Use an own recursive-descent parser (`src/sysml_icd/sysml/parser.py`) for the subset:
package, import, item/enum/attribute def, attribute usages, enum literals, doc, metadata annotations.
Unsupported constructs raise `ParseError` (fail loudly).

## Consequences
- No external dependency, fully testable.
- Must be replaced once models need ports, connections, expressions or constraints.
- Generators depend only on the internal data model, never on the parser, so it can be swapped.
