typedef struct { short vx; short vy; short vz; short pad; } SVECTOR;
typedef struct { int x; int y; int z; } _GsCOORDINATE2;
typedef struct Model { int a; SVECTOR rotate; } Model;
struct Holder {
    SVECTOR *svp;
    Model *mptr;
    void *vp;
};
void TakeS16(short *out);
void TakeCoord(_GsCOORDINATE2 *coord);
void TakeSame(SVECTOR *s);
void TakeVoid(void *p);
void test(struct Holder *h);
