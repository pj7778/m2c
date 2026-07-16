/* Context for the PSX unaligned whole-aggregate copy fold.
 * SVECTOR is sub-4-aligned (short fields), so gcc 2.7.2 copies it by value
 * using lwl/lwr + swl/swr word pairs. */
typedef struct { short vx, vy, vz, pad; } SVECTOR;

struct Src { SVECTOR v; };
struct Dst { SVECTOR v; };

/* d/s are typed as the same 8-byte aggregate: the word pairs fold to d->v = s->v.
 * vd/vs are void*: no aggregate type, so the fold must NOT fire and those stores
 * keep the M2C_UNALIGNED32 fallback (a genuinely-unaligned copy is never rewritten). */
void test(struct Dst *d, struct Src *s, void *vd, void *vs);
