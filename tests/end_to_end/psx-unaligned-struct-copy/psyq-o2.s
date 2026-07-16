.set noat
.set noreorder

# Two SVECTOR-sized (8-byte) copies made of lwl/lwr + swl/swr word pairs, the
# shape PSX gcc 2.7.2 emits for a sub-4-aligned struct assignment.

glabel test
    # d->v = s->v -- both ends are struct pointers to an 8-byte SVECTOR field,
    # so the two word pairs fold into a single aggregate assignment.
    lwl  $v0, 3($a1)
    lwr  $v0, 0($a1)
    lwl  $v1, 7($a1)
    lwr  $v1, 4($a1)
    swl  $v0, 3($a0)
    swr  $v0, 0($a0)
    swl  $v1, 7($a0)
    swr  $v1, 4($a0)
    # Same word pairs but through void* (vd=$a2, vs=$a3) -- no aggregate type
    # resolves, so the fold stays off and each store keeps the M2C_UNALIGNED32
    # fallback.
    lwl  $v0, 3($a3)
    lwr  $v0, 0($a3)
    lwl  $v1, 7($a3)
    lwr  $v1, 4($a3)
    swl  $v0, 3($a2)
    swr  $v0, 0($a2)
    swl  $v1, 7($a2)
    swr  $v1, 4($a2)
    jr   $ra
     nop
