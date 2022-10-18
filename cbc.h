#ifndef CBC_TEST
#define CBC_TEST
class CBC {
    unsigned char * last_block;

    public:
        CBC(unsigned long IV, void (*encrypt_algo)(), void (*decrypt_algo)());
        void set_message();
        unsigned char * encryp_next_block(unsigned char *);
        unsigned char * decrypt_next_block(unsigned char *);
};
#endif