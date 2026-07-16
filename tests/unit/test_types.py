import unittest

from m2c.types import StructDeclaration, Type


def _bitfield_struct(
    bitfields: "list[StructDeclaration.BitField]", size: int = 4
) -> StructDeclaration:
    return StructDeclaration(
        size=size,
        align=size,
        new_field_prefix="unk",
        tag_name="TEST",
        fields=[],
        bitfields=bitfields,
        has_bitfields=True,
    )


class TestGetFieldBitfields(unittest.TestCase):
    def test_byte_aligned_bitfield_resolves_to_named_field(self) -> None:
        """
        Mirrors PSX's P_TAG: `u32 addr:24; u32 len:8;`. Both the bit-offset (24)
        and width (8) of `len` are multiples of 8, so it compiles to a plain
        byte load/store just like an ordinary `u8 len` field would, and m2c
        should be able to name it.
        """
        struct = _bitfield_struct(
            [
                StructDeclaration.BitField(bit_offset=0, bit_width=24, name="addr"),
                StructDeclaration.BitField(bit_offset=24, bit_width=8, name="len"),
            ]
        )
        typ = Type.struct(struct)

        path, field_type, remaining_offset = typ.get_field(3, target_size=1)

        self.assertEqual(path, ["len"])
        self.assertEqual(remaining_offset, 0)
        self.assertEqual(field_type.get_size_bytes(), 1)

    def test_sub_byte_bitfield_still_bails(self) -> None:
        """
        `unsigned a:3; unsigned b:5;` packs two fields into a single byte with
        no byte-aligned boundary between them. This must keep bailing to
        `_no_matching_field()`, exactly as before this change.
        """
        struct = _bitfield_struct(
            [
                StructDeclaration.BitField(bit_offset=0, bit_width=3, name="a"),
                StructDeclaration.BitField(bit_offset=3, bit_width=5, name="b"),
            ]
        )
        typ = Type.struct(struct)

        path, field_type, remaining_offset = typ.get_field(0, target_size=1)

        self.assertIsNone(path)
        self.assertEqual(remaining_offset, 0)


if __name__ == "__main__":
    unittest.main()
