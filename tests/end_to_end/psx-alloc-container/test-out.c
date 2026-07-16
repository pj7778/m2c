Coord *test(void) {
    Model *temp_v0;

    temp_v0 = valloc(0x74U);
    temp_v0->tail[0] = 0;
    InitCoord((Coord *) temp_v0);
    return &temp_v0->locate;
}
