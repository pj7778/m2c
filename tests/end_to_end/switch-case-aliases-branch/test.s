.set noat      # allow manual use of $at
.set noreorder # don't insert nops after branches

# Distilled from tenchu-decomp's ActMOVE: a jump-table `case` entry aliases the
# SAME target as an ordinary (non-switch) branch that gets emitted earlier, by
# plain if/else flow, before the switch is even reached. Regression test for
# the "case label not within a switch statement" bug: build_switch_statement
# must emit a `case N: goto ...;` stub for such a case instead of relying on
# the target's real body (emitted outside the switch's braces) to carry the
# label.

.rdata
glabel jtbl_400200
.word .case0
.word .shared
.word .case2

.text
glabel test
# ordinary branch, unrelated to the switch: if a0 < 0, go straight to the
# node the switch's case 1 will also jump to
slti  $at, $a0, 0
bnez  $at, .shared
 nop
# fallthrough: a0 >= 0, dispatch on a0 in {0,1,2} via jump table
sltiu $at, $a0, 3
beqz  $at, .default
 sll   $t0, $a0, 2
lui   $at, %hi(jtbl_400200)
addu  $at, $at, $t0
lw    $t0, %lo(jtbl_400200)($at)
jr    $t0
 nop
.case0:
jr    $ra
 addiu $v0, $zero, 0x64
.shared:
jr    $ra
 addiu $v0, $zero, -1
.case2:
jr    $ra
 addiu $v0, $zero, 0xc8
.default:
jr    $ra
 move  $v0, $zero
