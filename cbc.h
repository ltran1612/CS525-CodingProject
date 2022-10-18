#ifndef CBC_TEST
#define CBC_TEST
class CBC {
    unsigned char * last_block;

    public:
        CBC(unsigned long IV, void (*encrypt_algo)(), void (*decrypt_algo)());
        unsigned char * encryp(unsigned char *);
        unsigned char * decrypt(unsigned char *);
}
#endif