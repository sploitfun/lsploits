...
#define unlink(P, BK, FD) {                                            \
    FD = P->fd;								      \
    BK = P->bk;								      \
    FD->bk = BK;							      \
    BK->fd = FD;							      \
    ...
}
...

