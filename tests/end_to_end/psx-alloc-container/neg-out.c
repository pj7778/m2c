Whole *test(void) {
    Whole *temp_v0;

    temp_v0 = valloc(0x74U);
    temp_v0->b[0] = 0;
    Process(temp_v0);
    return temp_v0;
}
