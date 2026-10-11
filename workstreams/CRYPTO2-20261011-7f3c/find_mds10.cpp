// Bounded search for one actual MDS matrix in a formerly uncovered order.
// Discovery uses Gaussian elimination and log tables. Independent validation
// in verify_mds.py uses all-minor Laplace recurrences and carryless products.
#include <cstdint>
#include <iostream>
#include <vector>
#include <stdexcept>
constexpr int N=10, Q=65536, POLY=0x1100b;
int logs[Q], exps[2*(Q-1)];
int mul(int a,int b){return a&&b?exps[logs[a]+logs[b]]:0;}
int divide(int a,int b){return a?exps[logs[a]-logs[b]+Q-1]:0;}
int countbits(int x){return __builtin_popcount((unsigned)x);}
bool minor(const int M[N][N],int rm,int cm){
 int A[N][N],r=0,c=0,k=countbits(rm);
 for(int i=0;i<N;i++)if(rm>>i&1){c=0;for(int j=0;j<N;j++)if(cm>>j&1)A[r][c++]=M[i][j];r++;}
 for(int i=0;i<k;i++){
  int p=i;while(p<k&&!A[p][i])p++;if(p==k)return false;
  for(int j=i;j<k;j++)std::swap(A[i][j],A[p][j]);
  for(int r=i+1;r<k;r++){int t=divide(A[r][i],A[i][i]);for(int j=i+1;j<k;j++)A[r][j]^=mul(t,A[i][j]);A[r][i]=0;}
 }
 return true;
}
int main(){
 int x=1;for(int i=0;i<Q-1;i++){if(i&&x==1)throw std::runtime_error("nonprimitive polynomial");logs[x]=i;exps[i]=x;x<<=1;if(x&Q)x^=POLY;}
 if(x!=1)throw std::runtime_error("invalid cycle");
 for(int i=Q-1;i<2*(Q-1);i++)exps[i]=exps[i-(Q-1)];
 std::vector<int> masks[N+1];for(int m=1;m<(1<<N);m++)masks[countbits(m)].push_back(m);
 uint64_t seed=202610117;
 for(int trial=1;trial<=200;trial++){
  int a[N],M[N][N];for(int i=0;i<N;i++){seed^=seed<<13;seed^=seed>>7;seed^=seed<<17;a[i]=(seed%(Q-1))+1;}
  for(int i=0;i<N;i++)for(int j=0;j<N;j++)M[i][j]=a[(i-j+N)%N];
  bool ok=true;int checked=0;
  for(int k=1;k<=N&&ok;k++)for(int r:masks[k]){if(!ok)break;for(int c:masks[k]){checked++;if(!minor(M,r,c)){ok=false;break;}}}
  if(ok){std::cout<<"{\"modulus\":"<<POLY<<",\"column\":[";for(int i=0;i<N;i++)std::cout<<(i?",":"")<<a[i];std::cout<<"],\"trial\":"<<trial<<",\"all_nonempty_square_minors\":"<<checked<<"}\n";return 0;}
 }
 std::cerr<<"No candidate in bounded 200-trial window\n";return 2;
}
