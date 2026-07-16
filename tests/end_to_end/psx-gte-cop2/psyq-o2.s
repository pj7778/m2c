.set noat
.set noreorder

glabel test
    addiu $sp, $sp, -0x20
    sw    $ra, 0x1C($sp)
    lwc2  $0, 0x0($a0)
    lwc2  $1, 0x4($a0)
    rtpt
    nclip
    avsz3
    cfc2  $v0, $31
    mfc2  $v1, $2
    swc2  $16, 0x0($a1)
    swc2  $17, 0x4($a1)
    swc2  $18, 0x8($a1)
    lw    $ra, 0x1C($sp)
    jr    $ra
     addiu $sp, $sp, 0x20
