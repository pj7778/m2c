/* A "leaf" struct (Coord, 0x50) and a "container" (Model, 0x74) embedding it at
 * offset 0. valloc(0x74) returns void*; the local is only ever unified to Coord*
 * via the InitCoord() parameter, yet the allocation size (0x74) names Model. With
 * --alloc-container-fn valloc, m2c types the local as Model* so the tail store at
 * 0x50 resolves to Model.tail instead of an unk50 on the wrong (Coord) tag. */
typedef struct Coord {
    int flg;
    int m[19];
} Coord;

typedef struct Model {
    struct Coord locate;
    int tail[9];
} Model;

/* A FLAT struct of the same size (0x74) whose offset-0 member is NOT an embedded
 * struct. It is not a container, so it never competes with Model for the size
 * match. When a local's field/param evidence already resolves it to Whole (a
 * complete 0x74 type), the size heuristic must leave it alone -- field-access
 * evidence wins over size. See neg.s. */
typedef struct Whole {
    int a[20];
    int b[9];
} Whole;

void *valloc(unsigned int size);
void InitCoord(Coord *c);
void Process(Whole *w);
