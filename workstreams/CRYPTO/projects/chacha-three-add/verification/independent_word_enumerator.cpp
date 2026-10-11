// Independent verifier, authored from the mathematical task specification.
// No discovery implementation or proof was read. All inputs are generated locally.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>

static uint32_t mask_for(unsigned n) {
    return n == 32 ? UINT32_MAX : ((uint32_t(1) << n) - 1);
}
static uint32_t rotate(uint32_t x, unsigned n, unsigned r, bool right = false) {
    r %= n;
    if (right && r) r = n - r;
    const uint32_t mask = mask_for(n);
    x &= mask;
    if (!r) return x;
    return ((x << r) | (x >> (n - r))) & mask;
}
static uint32_t output(uint32_t a, uint32_t b, uint32_t c, uint32_t d,
                       unsigned n, unsigned r, unsigned q,
                       bool linear, bool right = false) {
    const uint32_t mask = mask_for(n);
    const uint32_t s = linear ? (a ^ b) : ((a + b) & mask);
    const uint32_t t = rotate(d ^ s, n, r, right);
    const uint32_t u = linear ? (c ^ t) : ((c + t) & mask);
    const uint32_t v = rotate(b ^ u, n, q, right);
    return linear ? (s ^ v) : ((s + v) & mask);
}
static std::array<uint32_t,4> quarter_round(std::array<uint32_t,4> x) {
    auto &a=x[0], &b=x[1], &c=x[2], &d=x[3];
    a += b; d ^= a; d = rotate(d, 32, 16);
    c += d; b ^= c; b = rotate(b, 32, 12);
    a += b; d ^= a; d = rotate(d, 32, 8);
    c += d; b ^= c; b = rotate(b, 32, 7);
    return x;
}
int main() {
    const std::array<uint32_t,4> initial={0x11111111,0x01020304,0x9b8d6f43,0x01234567};
    const std::array<uint32_t,4> expected={0xea2a92f4,0xcb1cf8ce,0x4581472e,0x5881c4bb};
    const auto got=quarter_round(initial);
    if(got!=expected) { std::cerr << "RFC8439 vector failure\n"; return 2; }
    std::cout << "{\"kind\":\"rfc8439_section_2_1_1\",\"pass\":true,\"output_hex\":[";
    for(unsigned j=0;j<4;++j) { if(j) std::cout<<','; std::cout << '"' << std::hex << std::setw(8) << std::setfill('0') << got[j] << '"'; }
    std::cout << "]}\n" << std::dec;

    for(unsigned n=3;n<=5;++n) {
        const unsigned m=1u<<n;
        const uint64_t count=uint64_t(1)<<(4*n);
        // All rotations, including r=0, q=0 and wrapping indices, are retained.
        for(unsigned r=0;r<n;++r) for(unsigned q=0;q<n;++q) {
            std::array<int64_t,5> sums{};
            for(uint32_t a=0;a<m;++a) for(uint32_t b=0;b<m;++b)
            for(uint32_t c=0;c<m;++c) for(uint32_t d=0;d<m;++d) {
                const uint32_t error=output(a,b,c,d,n,r,q,false)^output(a,b,c,d,n,r,q,true);
                for(unsigned i=0;i<n;++i) sums[i] += ((error>>i)&1) ? -1 : 1;
            }
            std::cout << "{\"kind\":\"exhaustive\",\"n\":"<<n<<",\"r\":"<<r<<",\"q\":"<<q
                      <<",\"samples\":"<<count<<",\"signed_sums\":[";
            for(unsigned i=0;i<n;++i) { if(i)std::cout<<','; std::cout<<sums[i]; }
            std::cout<<"]}\n";
        }
    }
    // Deliberate wrong rotation convention, on a complete small input space.
    const unsigned n=5,r=1,q=2,i=3,m=1u<<n;
    int64_t sum=0;
    for(uint32_t a=0;a<m;++a) for(uint32_t b=0;b<m;++b)
    for(uint32_t c=0;c<m;++c) for(uint32_t d=0;d<m;++d) {
        const uint32_t err=output(a,b,c,d,n,r,q,false,true)^output(a,b,c,d,n,r,q,true,true);
        sum += ((err>>i)&1) ? -1 : 1;
    }
    std::cout << "{\"kind\":\"right_rotation_negative_control\",\"n\":5,\"r\":1,\"q\":2,\"i\":3,\"samples\":1048576,\"signed_sum\":"<<sum<<"}\n";
    return 0;
}
