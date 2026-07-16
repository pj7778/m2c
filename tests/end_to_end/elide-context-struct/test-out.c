/* m2c inferred field(s) in struct SomeStruct: ? unkC @ 0xC */

extern SomeStruct *glob2;

s16 test(void) {
    glob2 = &glob;
    glob2 = (SomeStruct *) &glob.unkC;
    return glob.unk100;
}
