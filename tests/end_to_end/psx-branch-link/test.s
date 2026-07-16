glabel test
bltzal $a0, .L1
nop
.L1:
bgezal $a1, .L2
nop
.L2:
jr $ra
nop
