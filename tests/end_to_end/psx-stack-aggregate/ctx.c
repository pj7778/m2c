typedef struct Param {
    int type;
    int user;
    int start;
    int end;
} Param;

void Use(Param *p);
void UseScalar(int *p);
void test(int a, int u);
