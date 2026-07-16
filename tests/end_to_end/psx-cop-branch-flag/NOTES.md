The `M2C_ERROR(/* Read from unset register $condition_bit */)` markers in
`test-out.c` are the **intended, accepted** output for this test, not a
regression or an open defect.

`bc0f`/`bc0t`/`bc2f`/`bc2t` branch on a coprocessor condition flag that only
COP1's compare instructions ever set in this codebase — nothing writes
`$condition_bit` for COP0 or COP2/GTE, so the condition's *source* is
genuinely unknown. What matters is that the branch itself is real (a proper
`if`, not silently dropped control flow) — see
`docs/superpowers/specs/2026-07-09-m2c-isa-completeness-design.md` in
tenchu-decomp for the "never crash, low fidelity is fine" bar this satisfies.

If this file's `M2C_ERROR` string shows up in a future grep for "still-broken"
cases, that grep is a false positive for this specific test.
