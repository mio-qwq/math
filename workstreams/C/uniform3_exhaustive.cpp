/*
 * Exact independent finite test for Agent C's uniform-order-three TF
 * automorphism obstruction. The universal lemma is proved in
 * mizzi_v3_uniform_odd.md; this code only checks the n=12 special case.
 *
 * 4 orbits of length 3; alpha(i,r)=(i,r+1 mod 3),
 * beta=alpha^{-1}. A undirected loopless graph invariant under
 * (alpha,beta) consists of an arbitrary union of the 18 orbit-pair
 * perfect matchings r+s = t (mod 3).
 *
 * C++20 standard library only, deterministic, fixed exhaustive space.
 */
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>

using namespace std;
constexpr int n = 12;
using Adj = array<uint16_t, n>;
struct Matching { array<pair<int,int>,3> e; };

array<Matching,18> build_matchings() {
    array<Matching,18> matches{};
    int index=0;
    for(int a=0;a<4;a++) for(int b=a+1;b<4;b++) for(int t=0;t<3;t++) {
        for(int r=0;r<3;r++) matches[index].e[r] = {3*a+r,3*b+(t-r+3)%3};
        index++;
    }
    assert(index==18);
    return matches;
}

void add_edge(Adj& adj,int u,int v) {
    assert(u != v && u>=0 && v>=0 && u<n && v<n);
    adj[u] |= uint16_t(1u<<v);
    adj[v] |= uint16_t(1u<<u);
}
void del_edge(Adj& adj,int u,int v) {
    adj[u] &= uint16_t(~(1u<<v)); adj[v] &= uint16_t(~(1u<<u));
}
Adj graph_from_mask(uint32_t mask, const array<Matching,18>& matchings) {
    Adj adj{};
    for(int t=0;t<18;t++) if((mask>>t)&1u)
        for(auto [u,v]:matchings[t].e) add_edge(adj,u,v);
    return adj;
}

bool connected(const Adj& adj) {
    int discovered=1, queue[n]={0}, count=1;
    for(int k=0;k<count;k++) {
        int u=queue[k];
        uint16_t neighbors=uint16_t(adj[u]&~discovered);
        while(neighbors) {
            int v=std::countr_zero(unsigned(neighbors));
            neighbors &= uint16_t(neighbors-1);
            discovered |= 1<<v;
            queue[count++]=v;
        }
    }
    return discovered==(1<<n)-1;
}
bool bipartite(const Adj& adj) {
    array<int,n> colors;
    colors.fill(-1);
    for(int root=0;root<n;root++) if(colors[root]<0) {
        int queue[n]={root}, count=1; colors[root]=0;
        for(int k=0;k<count;k++) {
            int u=queue[k];
            uint16_t neighbors=adj[u];
            while(neighbors) {
                int v=std::countr_zero(unsigned(neighbors));
                neighbors &= uint16_t(neighbors-1);
                if(colors[v]<0) { colors[v]=colors[u]^1; queue[count++]=v; }
                else if(colors[v]==colors[u]) return false;
            }
        }
    }
    return true;
}

bool path_closes_cycle(const Adj& adj,int first,int current,int visited,int depth,int length) {
    if(depth==length) return (adj[current]&(1<<first))!=0;
    // Restrict first to the minimum-index vertex on a simple cycle.
    uint16_t next=uint16_t(adj[current]&~visited & ~((1<<(first+1))-1));
    while(next) {
        int v=std::countr_zero(unsigned(next));
        next &= uint16_t(next-1);
        if(path_closes_cycle(adj,first,v,visited|(1<<v),depth+1,length)) return true;
    }
    return false;
}
bool has_simple_cycle(const Adj& adj,int length) {
    assert(length>=3 && length<=n);
    for(int first=0;first<n;first++) {
        uint16_t next=uint16_t(adj[first]&~((1<<(first+1))-1));
        while(next) {
            int v=std::countr_zero(unsigned(next));
            next &= uint16_t(next-1);
            if(path_closes_cycle(adj,first,v,(1<<first)|(1<<v),2,length)) return true;
        }
    }
    return false;
}

bool tf_auto(const Adj& adj) {
    // Verify from the ORIGINAL ordered adjacency relation, not orbit labels.
    auto alpha=[](int u){return 3*(u/3)+(u%3+1)%3;};
    auto beta=[](int u){return 3*(u/3)+(u%3+2)%3;};
    for(int u=0;u<n;u++) for(int v=0;v<n;v++) {
        bool before=(adj[u]&(1<<v))!=0;
        bool after=(adj[alpha(u)]&(1<<beta(v)))!=0;
        if(before != after) return false;
    }
    return true;
}

void sanity_tests(const array<Matching,18>& ms) {
    Adj tri{};add_edge(tri,0,1);add_edge(tri,1,2);add_edge(tri,2,0);
    assert(has_simple_cycle(tri,3)); assert(!has_simple_cycle(tri,6));
    Adj hex{};for(int i=0;i<6;i++) add_edge(hex,i,(i+1)%6);
    assert(has_simple_cycle(hex,6));assert(!has_simple_cycle(hex,3));
    Adj pent{};for(int i=0;i<5;i++) add_edge(pent,i,(i+1)%5);
    assert(has_simple_cycle(pent,5));assert(!has_simple_cycle(pent,6));
    Adj line{};for(int i=0;i<10;i++)add_edge(line,i,i+1);
    assert(!has_simple_cycle(line,3));assert(!has_simple_cycle(line,6));
    Adj witness=graph_from_mask(122241u,ms);
    assert(tf_auto(witness));
    del_edge(witness,0,3);
    assert(!tf_auto(witness));  // Intentional damaged-edge negative test.
}
int main() {
    auto ms=build_matchings();
    sanity_tests(ms);
    int searched=0,all_connected=0,all_nonbip=0,triangle=0,sixcycle=0,exception=0;
    for(uint32_t mask=0;mask<(1u<<18);mask++) {
        if(std::popcount(mask)<4)continue; // 0..3 matchings have <=9 edges, cannot connect 12 vertices.
        searched++;
        auto A=graph_from_mask(mask,ms);
        if(!connected(A))continue;
        all_connected++;
        if(bipartite(A))continue;
        all_nonbip++;
        bool has3=has_simple_cycle(A,3),has6=has_simple_cycle(A,6);
        if(has3)triangle++;
        if(has6)sixcycle++;
        if(!(has3&&has6)) { exception++;cerr<<"COUNTEREXAMPLE mask="<<mask<<'\n'; }
    }
    cout << "exhaustive_orbit_masks=" << (1u<<18) << '\n';
    cout << "checked_connected_possible=" << searched << '\n';
    cout << "connected=" << all_connected << '\n';
    cout << "connected_nonbipartite=" << all_nonbip << '\n';
    cout << "connected_nonbipartite_with_C3=" << triangle << '\n';
    cout << "connected_nonbipartite_with_C6=" << sixcycle << '\n';
    cout << "counterexample_to_subfamily_lemma=" << exception << '\n';
    cout << "negative_tests=" << 5 << " passed\n";
    if(exception!=0 || all_nonbip!=245764 || all_connected!=257942)return 1;
}
