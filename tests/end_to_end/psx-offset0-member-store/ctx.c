struct Param {
    int type;
    int user;
};

void Use(struct Param *p);

/* A context-provided stack struct: the slot at 0x10 is a known `struct Param`,
   NOT an inferred/synthesized aggregate. A scalar store to offset 0x10 targets
   Param.type (offset 0), and must render as the member `sp10.type = ...`, never
   as the bare aggregate `sp10 = ...` (assigning an int to a struct -- invalid C,
   the offset-0 field-elision bug). `&sp10` (whole object) must still declare the
   `Param sp10` local. */
struct _m2c_stack_test {
    char pad0[0x10];
    struct Param p;
    char pad1[8];
};

void test(int u);
