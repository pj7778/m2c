import unittest

from m2c.flow_graph import InstrRef
from m2c.instruction import Instruction, InstructionMeta
from m2c.source_annotate import format_source_annotation


def _instr(mnemonic: str, meta: InstructionMeta) -> Instruction:
    return Instruction(
        mnemonic=mnemonic,
        args=[],
        meta=meta,
        inputs=[],
        clobbers=[],
        outputs=[],
        eval_fn=None,
    )


def _ref(instr: Instruction) -> InstrRef:
    # format_source_annotation only reads .instruction; `block` is unused by
    # the code under test, so a real Block isn't needed for this fixture.
    return InstrRef(instr, None)  # type: ignore[arg-type]


class TestFormatSourceAnnotation(unittest.TestCase):
    def test_real_instruction_formats_file_and_line(self) -> None:
        meta = InstructionMeta(
            emit_goto=False, filename="AddPrim.s", lineno=12, synthetic=False
        )
        ref = _ref(_instr("jr", meta))
        self.assertEqual(format_source_annotation(ref), "/* AddPrim.s:12: jr */")

    def test_synthetic_instruction_has_no_annotation(self) -> None:
        meta = InstructionMeta(
            emit_goto=False, filename="AddPrim.s", lineno=12, synthetic=True
        )
        ref = _ref(_instr("jr", meta))
        self.assertIsNone(format_source_annotation(ref))

    def test_no_current_instruction_has_no_annotation(self) -> None:
        self.assertIsNone(format_source_annotation(None))


if __name__ == "__main__":
    unittest.main()
