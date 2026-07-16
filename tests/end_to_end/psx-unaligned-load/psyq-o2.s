.set noat
.set noreorder

glabel test
    /* lwr before lwl — PSX LE unaligned load pattern */
    lwr  $v0, 1($a0)
    lwl  $v0, 4($a0)
    jr   $ra
     nop
