# Regression test: GCC needs a temp register to move $sp by more than 0x7FFF
# bytes (`lui`/`ori`+`subu`, already handled by get_stack_info), and then, for
# a frame this large, reuses that same constant added back to the (already
# adjusted) $sp to recompute the pre-adjustment $sp in a fresh register
# ($t5 here via `addu`). The prologue's callee-save stores then use *that*
# register as their base, with small negative offsets, instead of an offset
# from $sp that wouldn't fit in a 16-bit immediate. Mirrors the real-world
# KPRINTF_OBJ_140 case. Two things must both hold:
#  - is_leaf must still be recognized as false (from the $ra save through the
#    aliased base), so the stack-passed call argument below resolves instead
#    of erroring "Unable to find stack arg".
#  - the callee-save stores/restores through the aliased base must resolve as
#    ordinary stack locations, not as field accesses on a phantom "argument"
#    (get_stack_var's above-the-frame check triggers exactly at this
#    register's value, since it equals allocated_stack_size).
# `foo` takes 5 int params: a-d in $a0-$a3, e at sp+0x10 (the first
# stack-passed argument slot).

glabel test
lui   $t4, 1
ori   $t4, $t4, 0x20
subu  $sp, $sp, $t4
addu  $t5, $t4, $sp
sw    $ra, -0x4($t5)
sw    $s0, -0x8($t5)
addiu $s0, $a0, 1
addiu $a0, $zero, 1
addiu $a1, $zero, 2
addiu $a2, $zero, 3
sw    $s0, 0x10($sp)
jal   foo
addiu $a3, $zero, 4
lui   $t4, 1
ori   $t4, $t4, 0x20
addu  $t5, $t4, $sp
lw    $ra, -0x4($t5)
lw    $s0, -0x8($t5)
addiu $v0, $zero, 0
jr    $ra
addu  $sp, $sp, $t4
