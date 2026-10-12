// Independent second algorithm. No carry propagation and no author imports.
// Uses D(mask) = { mask - 2*s modulo 2^32 : s is a submask of mask }.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>

using U = std::uint32_t;
U rr(U x, unsigned n) { return (x >> n) | (x << (32-n)); }
U f(U x) { return rr(x,7) ^ rr(x,18) ^ (x>>3); }
U g(U x) { return rr(x,17) ^ rr(x,19) ^ (x>>10); }

std::vector<U> values(U mask) {
    std::set<U> out;
    U s = mask;
    for (;;) {
        out.insert(mask - U(2)*s);
        if (s==0) break;
        s=(s-1)&mask;
    }
    return {out.begin(),out.end()};
}

bool contains(U mask, U delta) {
    // 2*s == mask-delta mod 2^32 has precisely the following two solutions.
    U twice = mask-delta;
    if (twice & 1) return false;
    U low = twice>>1;
    U high = low | U(0x80000000);
    return (low & ~mask)==0 || (high & ~mask)==0;
}

int verify(int argc, char** argv) {
    if (argc!=2) throw std::runtime_error("usage: check_subsets kernel-masks.txt");
    std::ifstream stream(argv[1]);
    if (!stream) throw std::runtime_error("missing kernel packet");
    std::set<U> masks;
    std::size_t records=0;
    std::uint64_t input;
    while (stream >> std::hex >> input) {
        if (input>UINT32_MAX) throw std::runtime_error("word outside 32 bits");
        U mask=static_cast<U>(input);
        if ((f(mask)&0xffff)!=0) throw std::runtime_error("nonkernel mask");
        masks.insert(mask); ++records;
    }
    if (!stream.eof() || records!=65536 || masks.size()!=65536)
        throw std::runtime_error("incomplete or duplicate kernel packet");
    U K=0x44ab0000;
    if ((K&0xffff) || (g(K)&0xffff)) throw std::runtime_error("wrong K");
    auto first_values=values(f(K));
    std::vector<U> first;
    for (U L:masks) {
        bool possible=false;
        for (U fx:first_values) {
            if (contains(L,U(0)-fx)) { possible=true; break; }
        }
        if (possible) first.push_back(L);
    }
    std::vector<U> expected{0x4804ddd6,0x5804fff6,0xc814ddf6,0xd805eee6,0xd814ffd6};
    if (first!=expected) throw std::runtime_error("wrong first survivors");
    auto a_values=values(K), c_values=values(g(K));
    for (U m:{U(1),U(2)}) {
        unsigned surviving=0;
        for (U L:first) {
            bool possible=false;
            for (U a:a_values) for (U c:c_values)
                if (contains(f(L),U(0)-m*a-c)) possible=true;
            surviving+=possible;
        }
        if (surviving) throw std::runtime_error("second equality survived");
        std::cout << "m=" << m << " second_survivors=" << surviving << "\n";
    }
    // Independent exact membership checks at all 8-bit masks and residues.
    for (U mask=0;mask<256;++mask) {
        auto exact=values(mask);
        for (U delta=0;delta<256;++delta) {
            bool target=std::binary_search(exact.begin(),exact.end(),delta);
            if (contains(mask,delta)!=target)
                throw std::runtime_error("membership control failed");
        }
    }
    std::cout << "algorithm=submask-membership kernel_records=" << records
              << " first_survivors=" << first.size()
              << " fK_distinct_differences=" << first_values.size()
              << " membership_controls=65536\n";
    return 0;
}

int main(int argc, char** argv) {
    try {
        return verify(argc,argv);
    } catch (const std::exception& error) {
        std::cerr << "REJECT: " << error.what() << "\n";
        return 1;
    }
}
