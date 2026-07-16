/* PSX little-endian unaligned 32-bit load (lwr before lwl) */
typedef struct {
    char pad;       /* offset 0 */
    int  value;     /* offset 1 — unaligned */
} UnalignedStruct;

int get_value(UnalignedStruct *s) {
    return s->value;
}
