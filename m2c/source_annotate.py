"""Render a per-statement source-instruction annotation comment.

Every `Instruction` already carries everything needed to point back at
exactly where it came from -- `meta.filename`/`meta.lineno` (the asm source
location) plus its own `mnemonic`/`args` -- but none of it survives into
the final decompiled C today. `RegInfo` (translate.py) already tracks
"the instruction currently being processed" throughout the whole
per-instruction translation loop (`current_instr_ref()`/`has_current_instr()`,
used today only for error messages), which is the same information this
needs -- so wiring this in is a matter of reading that existing state at
the one place every `Statement` gets appended to a block
(`RegInfo.write_statement`), not adding new tracking.

Kept as its own module (not inlined into translate.py) so it can be
reviewed/tested independently of translate.py's per-instruction
evaluation logic.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .flow_graph import InstrRef


def format_source_annotation(instr_ref: Optional["InstrRef"]) -> Optional[str]:
    """Return a `/* ... */` comment pointing at the asm instruction INSTR_REF
    came from, or None if there's nothing real to point at (no instruction
    was current, or it's synthetic -- e.g. a pattern-matched/derived
    instruction with no direct asm source line, per
    `InstructionMeta.synthetic`).

    Format: `/* FILE:LINE: mnemonic arg1, arg2 */` -- FILE:LINE matches
    the exact line in the prepped asm this project's `just diagnose-crash`/
    `just diff` workflow already opens when cross-referencing a mismatch,
    and `str(instruction)` is the same rendering m2c's own error messages
    already use (see `InstrProcessingFailure.__str__`), so this isn't a new
    format to learn -- it's the same one already seen in error output,
    just now attached to successful statements too.
    """
    if instr_ref is None:
        return None
    instr = instr_ref.instruction
    if instr.meta.synthetic:
        return None
    return f"/* {instr.meta.filename}:{instr.meta.lineno}: {instr} */"
