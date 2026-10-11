#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

// Independent direct word enumeration. No borrow/carry state machine occurs here.
static std::uint32_t rol(std::uint32_t x, unsigned r, unsigned n) {
    const std::uint32_t mask = (std::uint32_t{1} << n) - 1;
    r %= n;
    if (r == 0) return x & mask;
    return ((x << r) | (x >> (n - r))) & mask;
}

static std::uint32_t difference(std::uint32_t a, std::uint32_t b,
                                std::uint32_t c, std::uint32_t d,
                                unsigned n, unsigned r, unsigned q) {
    const std::uint32_t mask = (std::uint32_t{1} << n) - 1;
    const std::uint32_t s = (a + b) & mask;
    const std::uint32_t t = rol(d ^ s, r, n);
    const std::uint32_t u = (c + t) & mask;
    const std::uint32_t v = rol(b ^ u, q, n);
    const std::uint32_t w = (s + v) & mask;

    const std::uint32_t linear_s = a ^ b;
    const std::uint32_t linear_t = rol(d ^ linear_s, r, n);
    const std::uint32_t linear_u = c ^ linear_t;
    const std::uint32_t linear_v = rol(b ^ linear_u, q, n);
    const std::uint32_t linear_w = linear_s ^ linear_v;
    return w ^ linear_w;
}

int main() {
    for (unsigned n = 1; n <= 4; ++n) {
        const std::uint32_t size = std::uint32_t{1} << n;
        const std::uint64_t samples = std::uint64_t{1} << (3 * n);
        for (unsigned r = 0; r < n; ++r) {
            for (unsigned q = 0; q < n; ++q) {
                for (std::uint32_t a = 0; a < size; ++a) {
                    std::vector<std::int64_t> signed_sums(n, 0);
                    for (std::uint32_t b = 0; b < size; ++b) {
                        for (std::uint32_t c = 0; c < size; ++c) {
                            for (std::uint32_t d = 0; d < size; ++d) {
                                const auto e = difference(a, b, c, d, n, r, q);
                                for (unsigned i = 0; i < n; ++i) {
                                    signed_sums[i] += ((e >> i) & 1) ? -1 : 1;
                                }
                            }
                        }
                    }
                    std::cout << "{\"kind\":\"fixed_a_exhaustive\",\"n\":" << n
                              << ",\"r\":" << r << ",\"q\":" << q
                              << ",\"a\":" << a << ",\"samples\":" << samples
                              << ",\"signed_sums\":[";
                    for (unsigned i = 0; i < n; ++i) {
                        if (i) std::cout << ',';
                        std::cout << signed_sums[i];
                    }
                    std::cout << "]}\n";
                }
            }
        }
    }
}
