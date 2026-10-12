#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <vector>

struct Clause { std::vector<int> lits; };

int main(int argc, char **argv) {
  if (argc != 4) {
    std::cerr << "usage: walksat input.cnf output.bits seconds\n";
    return 2;
  }
  std::ifstream in(argv[1]);
  std::string line;
  int nvars = 0, nclauses = 0;
  std::vector<Clause> clauses;
  while (std::getline(in, line)) {
    if (line.empty() || line[0] == 'c') continue;
    if (line[0] == 'p') {
      std::istringstream ss(line); std::string p, cnf;
      ss >> p >> cnf >> nvars >> nclauses;
      clauses.reserve(nclauses);
      continue;
    }
    std::istringstream ss(line); int lit; Clause c;
    while (ss >> lit && lit) c.lits.push_back(lit);
    if (!c.lits.empty()) clauses.push_back(std::move(c));
  }
  if ((int)clauses.size() != nclauses) return 3;
  std::vector<std::vector<int>> occurs(2 * nvars);
  for (int ci = 0; ci < nclauses; ++ci)
    for (int lit : clauses[ci].lits)
      occurs[2 * (std::abs(lit) - 1) + (lit < 0)].push_back(ci);

  const double seconds = std::stod(argv[3]);
  auto deadline = std::chrono::steady_clock::now() +
                  std::chrono::milliseconds((long long)(seconds * 1000));
  std::mt19937_64 rng(0x534841323536ULL);
  std::vector<uint8_t> value(nvars), fixed(nvars, 0);
  for (const auto &c : clauses) if (c.lits.size() == 1) {
    int lit = c.lits[0], v = std::abs(lit) - 1;
    value[v] = lit > 0; fixed[v] = 1;
  }
  std::vector<int> count(nclauses), unsat, where(nclauses, -1);
  auto lit_true = [&](int lit) { return value[std::abs(lit)-1] == (lit > 0); };
  auto add_unsat = [&](int c) {
    if (where[c] < 0) { where[c] = unsat.size(); unsat.push_back(c); }
  };
  auto del_unsat = [&](int c) {
    if (where[c] >= 0) {
      int p = where[c], last = unsat.back(); unsat[p] = last; where[last] = p;
      unsat.pop_back(); where[c] = -1;
    }
  };
  uint64_t flips = 0, restarts = 0;
  while (std::chrono::steady_clock::now() < deadline) {
    ++restarts;
    for (int v = 0; v < nvars; ++v) if (!fixed[v]) value[v] = rng() & 1;
    unsat.clear(); std::fill(where.begin(), where.end(), -1);
    for (int c = 0; c < nclauses; ++c) {
      count[c] = 0; for (int lit : clauses[c].lits) count[c] += lit_true(lit);
      if (!count[c]) add_unsat(c);
    }
    for (uint64_t step = 0; step < 3000000 && !unsat.empty(); ++step, ++flips) {
      int ci = unsat[rng() % unsat.size()];
      std::vector<int> candidates;
      for (int lit : clauses[ci].lits) if (!fixed[std::abs(lit)-1])
        candidates.push_back(std::abs(lit)-1);
      if (candidates.empty()) break;
      int chosen = candidates[rng() % candidates.size()];
      if ((rng() % 100) >= 45) {
        int best = 1 << 30;
        std::shuffle(candidates.begin(), candidates.end(), rng);
        for (int v : candidates) {
          int break_count = 0;
          int true_sign = value[v] ? 0 : 1;
          for (int c : occurs[2*v + true_sign]) break_count += count[c] == 1;
          if (break_count < best) { best = break_count; chosen = v; }
        }
      }
      int old_true_sign = value[chosen] ? 0 : 1;
      int new_true_sign = 1 - old_true_sign;
      for (int c : occurs[2*chosen + old_true_sign]) {
        if (--count[c] == 0) add_unsat(c);
      }
      value[chosen] ^= 1;
      for (int c : occurs[2*chosen + new_true_sign]) {
        if (count[c]++ == 0) del_unsat(c);
      }
    }
    if (unsat.empty()) {
      std::ofstream out(argv[2]);
      for (int v = 0; v < nvars; ++v) out << int(value[v]) << '\n';
      std::cerr << "SAT flips=" << flips << " restarts=" << restarts << "\n";
      return 0;
    }
  }
  std::cerr << "UNKNOWN flips=" << flips << " restarts=" << restarts << "\n";
  return 1;
}
