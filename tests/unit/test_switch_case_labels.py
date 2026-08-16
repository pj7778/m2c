"""Guards for build_switch_statement's handling of context.case_nodes.

7b480c5's _case_label_for_switch assumed every node reaching build_switch_statement
as a `case` of this switch has EXACTLY ONE registered label. That was wrong in both
directions, and both directions caused real damage on King's Field:

  - zero:  add_labels_for_switch deliberately skips registering a target that is an
           empty goto to the default node / the switch's postdominator, and only
           restores those skipped labels when the switch has fewer than 5 real ones.
           Such a target still arrives in `cases`. FUN_80038a38 hit this and the
           whole function failed to decompile (DecompFailure).
  - many:  several jump-table entries can share one target, each registering its own
           label. Emitting only the first and unregistering the rest silently routed
           the others to `default:` -- wrong C, no error. FUN_8002edd4 lost 8 cases,
           and tests/end_to_end/multi-switch/irix-o2-noswitch had it frozen into its
           checked-in snapshot for a month.

The end-to-end trigger needs a 93KB function plus a 63KB typed context (it does not
reproduce without --context, and hand-distilling collapses the shared node before it
can be emitted early), so the bookkeeping is pinned here directly instead.

WHICH OF THESE ARE REGRESSION GUARDS, AND WHICH ARE ONLY SMOKE TESTS
-------------------------------------------------------------------
A test that exercises code INTRODUCED BY the fix cannot fail on the code before
it -- it errors on a missing attribute instead, or does not run at all. Such a
test is green, is about the right code, and would have caught nothing. Stating
which is which here, because the distinction is invisible from a passing run:

  REGRESSION GUARDS -- verified to FAIL against the pre-fix commit c167f4b:
    test_zero_registrations_does_not_fail      (errors with the original
                                                "no case label registered for
                                                node 5 in its own case list")
    test_all_shared_labels_are_emitted         (fails with "'case 9:' not found
                                                in 'case 1:\ngoto block_7;'")

  SMOKE TESTS ONLY -- they exercise mark_emitted/switch_stack, which do not
  exist before f1d9790, so they cannot be run against it:
    test_case_emitted_inside_a_NESTED_switch_is_foreign
    test_case_emitted_directly_in_this_switch_stays_put

  A node is only foreign if it ALSO carries a label to jump to -- these
  fixtures must add to `labeled_nodes` as well as `emitted_nodes`, because real
  emission (emit_node) does both, and a goto to an unlabelled node dangles.

  The real guard for the nesting rule is the King's Field corpus check
  `just m2c-validity`, which DOES fail on the pre-fix build and names both
  offenders (FUN_80038a38 and FUN_80036af0). Corpus over fixture, whenever the
  fixture would have to be built out of the fix's own vocabulary.
"""

import unittest
from types import SimpleNamespace

from m2c.flow_graph import BasicNode, Block
from m2c.if_statements import Context, SwitchStatement, build_switch_statement
from m2c.options import Formatter
from m2c.translate import SwitchControl


def _node(index: int) -> BasicNode:
    """A node standing on its own: build_switch_statement only ever looks at
    `block.index` (case ordering), `loop` (label naming) and identity."""
    block = Block(index=index, label=None, approx_label_name=f"blk{index}")
    node = BasicNode(block=block, emit_goto=False, successor=None)  # type: ignore[arg-type]
    return node


def _context() -> Context:
    # build_switch_statement reads only options.debug and never touches
    # flow_graph on these paths; a real Options needs 45 arguments.
    return Context(
        flow_graph=None,  # type: ignore[arg-type]
        fmt=Formatter(),
        options=SimpleNamespace(debug=False),  # type: ignore[arg-type]
    )


def _switch_body_text(stmt: SwitchStatement) -> str:
    fmt = Formatter()
    return "\n".join(
        s.format(fmt) for s in stmt.body.statements if s.should_write()
    )


class TestSwitchCaseLabels(unittest.TestCase):
    def test_zero_registrations_does_not_fail(self) -> None:
        """A case with NO label registered for this switch is not an internal
        inconsistency: add_labels_for_switch skipped it on purpose. It must be
        passed over quietly, not raise. (King's Field FUN_80038a38.)"""
        context = _context()
        end = _node(99)
        skipped = _node(5)
        switch_node = _node(0)
        switch_index = context.add_switch(switch_node)

        # The exact broken state: `skipped` is a case of this switch, was emitted
        # before the switch's own body-building started, and has no registration.
        context.emitted_nodes.add(skipped)
        self.assertEqual(context.case_nodes[skipped], [])

        stmt = build_switch_statement(
            context,
            SwitchControl(control_expr=None),  # type: ignore[arg-type]
            [skipped],
            switch_index,
            end,
        )
        # Nothing to emit for it -- `default:` covers those values.
        self.assertNotIn("case", _switch_body_text(stmt))

    def test_all_shared_labels_are_emitted(self) -> None:
        """When several jump-table entries share one foreign target, EVERY label
        must be emitted before the goto. Emitting only the first silently routes
        the rest to `default:`. (King's Field FUN_8002edd4 lost 8 cases.)"""
        context = _context()
        end = _node(99)
        shared = _node(7)
        switch_node = _node(0)
        switch_index = context.add_switch(switch_node)

        context.emitted_nodes.add(shared)
        context.labeled_nodes.add(shared)  # emit_node does both; see Context
        for label in ("case 1", "case 9", "case 10"):
            context.case_nodes[shared].append((switch_index, label))

        stmt = build_switch_statement(
            context,
            SwitchControl(control_expr=None),  # type: ignore[arg-type]
            [shared],
            switch_index,
            end,
        )

        text = _switch_body_text(stmt)
        for label in ("case 1:", "case 9:", "case 10:"):
            self.assertIn(label, text)
        # ...routed by a single goto, and unregistered so the foreign site does
        # not print `case N:` a second time where it is invalid.
        self.assertEqual(text.count("goto "), 1)
        self.assertEqual(context.case_nodes[shared], [])

    def test_case_emitted_inside_a_NESTED_switch_is_foreign(self) -> None:
        """The direction the emission-order heuristic missed, and the one that
        produced uncompilable C on King's Field FUN_80038a38.

        A node emitted while building THIS switch's body is not automatically
        contained: if it landed inside a switch NESTED in this one, our label
        there is invalid ("multiple default labels in one switch" -- gcc). Only
        the innermost enclosing switch may place a label, so an outer switch
        must fall back to a goto stub."""
        context = _context()
        end = _node(99)
        shared = _node(7)
        outer = context.add_switch(_node(0))
        inner = context.add_switch(_node(1))
        context.case_nodes[shared].append((outer, "default"))

        # Emitted while `inner` was the innermost switch being built.
        context.switch_stack.append(inner)
        context.mark_emitted(shared)
        context.labeled_nodes.add(shared)  # emit_node does both; see Context
        context.switch_stack.pop()

        stmt = build_switch_statement(
            context,
            SwitchControl(control_expr=None),  # type: ignore[arg-type]
            [shared],
            outer,
            end,
        )
        text = _switch_body_text(stmt)
        self.assertIn("default:", text)
        self.assertIn("goto ", text)
        # ...and unregistered, so the nested site does not ALSO print it there.
        self.assertEqual(context.case_nodes[shared], [])

    def test_case_emitted_directly_in_this_switch_stays_put(self) -> None:
        """The converse: owned by THIS switch, so its own label is valid where it
        already is and no stub is needed. Guards against the fix above
        over-firing and turning every shared case into a goto."""
        context = _context()
        end = _node(99)
        owned = _node(7)
        switch_index = context.add_switch(_node(0))
        context.case_nodes[owned].append((switch_index, "case 1"))

        context.switch_stack.append(switch_index)
        context.mark_emitted(owned)
        context.switch_stack.pop()

        stmt = build_switch_statement(
            context,
            SwitchControl(control_expr=None),  # type: ignore[arg-type]
            [owned],
            switch_index,
            end,
        )
        self.assertNotIn("goto ", _switch_body_text(stmt))
        self.assertEqual(context.case_nodes[owned], [(switch_index, "case 1")])

    def test_other_switches_registrations_are_untouched(self) -> None:
        """Unregistering must be scoped to this switch: a node shared with a
        second switch keeps that switch's label."""
        context = _context()
        end = _node(99)
        shared = _node(7)
        switch_index = context.add_switch(_node(0))
        other_index = context.add_switch(_node(1))

        context.emitted_nodes.add(shared)
        context.labeled_nodes.add(shared)  # emit_node does both; see Context
        context.case_nodes[shared].append((switch_index, "case 1"))
        context.case_nodes[shared].append((other_index, "case 2"))

        build_switch_statement(
            context,
            SwitchControl(control_expr=None),  # type: ignore[arg-type]
            [shared],
            switch_index,
            end,
        )
        self.assertEqual(context.case_nodes[shared], [(other_index, "case 2")])


if __name__ == "__main__":
    unittest.main()
