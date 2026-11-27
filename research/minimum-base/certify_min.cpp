#include <bits/stdc++.h>
using namespace std; using ll=long long;
int powmod(ll a,ll b,int m){ll r=1;for(;b;b>>=1,a=a*a%m)if(b&1)r=r*a%m;return r;}
int inv(int a,int m){ll x=1,y=0,b=m;while(b){ll q=a/b;ll t=a-q*b;a=b;b=t;t=x-q*y;x=y;y=t;}if(a!=1)abort();return (x%m+m)%m;}
struct Mod{int q;vector<unsigned char> ok;double density;};
vector<Mod> filters(int n,int p,int s,const vector<int>& primes){vector<Mod> ms;for(int q:primes){if(q>min(5000,max(500,24*p+1)))break;if(q>103&&q!=p&&(q-1)%p)continue;vector<int> v(q);for(int a=0;a<q;a++)v[a]=powmod(a,p,q);vector<unsigned char> ok((ll)q*q);ll cnt=0;vector<unsigned char> t(q),t0(q);for(int d=0;d<q;d++){
 fill(t.begin(),t.end(),0);fill(t0.begin(),t0.end(),0);
 for(int y=0;y<q;y++){int z=(y+d)%q;if(!y&&!z)continue;int g=(v[z]-v[y]+q)%q;t[g]=1;if(y&&z)t0[g]=1;}
 for(int x=0;x<q;x++){int g=(v[x]+s*(n%q)+q)%q;bool pass=x?t[g]:t0[g];ok[(ll)d*q+x]=pass;cnt+=pass;}}
 // Floating point is only used for filter ordering/selection, never to reject an individual candidate.
 double density=double(cnt)/((ll)q*q);if(density<0.98)ms.push_back({q,move(ok),density});}
 sort(ms.begin(),ms.end(),[](auto&a,auto&b){return a.density<b.density;});return ms;}
// All x mod d with x^p = -s*N mod d, by prime-power lifting and CRT.
vector<vector<int>> roots(int n,int p,int s,int D,const vector<int>& spf){vector<vector<int>> r(D+1);r[1]={0};for(int d=2;d<=D;d++){
 int q=spf[d], m=d/q, target=(int)((-(ll)s*n%d+d)%d);
 if(m==1){if(q!=p&&(q-1)%p){int a=target?powmod(target,inv(p%(q-1),q-1),q):0; if(q==2)a=target;r[d]={a};}else if(!target)r[d]={0};else if(q==p)r[d]={target};else if(powmod(target,(q-1)/p,q)==1){int k=(q-1)/p;if(k%p){int root=powmod(target,inv(p%k,k),q);int h=1;for(int g=2;h==1;g++)h=powmod(g,k,q);for(int i=0;i<p;i++){r[d].push_back(root);root=(ll)root*h%q;}}else for(int a=1;a<q;a++)if(powmod(a,p,q)==target)r[d].push_back(a);}}
 else if(m%q==0){int b=m;while(b%q==0)b/=q;if(b==1){for(int a:r[m])for(int t=0;t<q;t++)if(powmod(a+t*m,p,d)==target)r[d].push_back(a+t*m);}else{int h=d/b;int hi=inv(h%b,b);for(int a:r[h])for(int c:r[b])r[d].push_back(a+(ll)h*((ll)((c-a%b+b)%b)*hi%b));}}
 else {int mi=inv(m%q,q);for(int a:r[m])for(int c:r[q])r[d].push_back(a+(ll)m*((ll)((c-a%q+q)%q)*mi%q));}
 }
 // Independently check cardinality, distinctness, and validity of every root set.
 vector<int> counts(D+1);counts[1]=1;
 for(int d=2;d<=D;d++){
   int q=spf[d],b=d,e=0,qe=1;while(b%q==0){b/=q;qe*=q;e++;}
   int target=(int)((-(ll)s*n%qe+qe)%qe),count=0;
   if(target==0){count=1;for(int i=0;i<e-(e+p-1)/p;i++)count*=q;}
   else if(target%q==0){int v=0,t=n;while(t%q==0){t/=q;v++;}if(v>=p)abort();count=0;}
   else if(q==2)count=1;
   else {int phi=qe-qe/q,g=gcd(p,phi);count=powmod(target,phi/g,qe)==1?g:0;}
   counts[d]=count*counts[b];
   sort(r[d].begin(),r[d].end());
   if((int)r[d].size()!=counts[d]||adjacent_find(r[d].begin(),r[d].end())!=r[d].end())abort();
   int fulltarget=(int)((-(ll)s*n%d+d)%d);
   for(int a:r[d])if(a<0||a>=d||powmod(a,p,d)!=fulltarget)abort();
 }
 return r;}
int main(int argc,char**argv){int B=argc>1?stoi(argv[1]):10000000;if(B<1000||B>10000000){cerr<<"B must be in [1000,10000000]\n";return 2;}int maxp=B/5;int M=max(5000,maxp);vector<int> spf(M+1),primes;for(int i=2;i<=M;i++){if(!spf[i]){spf[i]=i;primes.push_back(i);}for(int q:primes){if(q>spf[i]||(ll)i*q>M)break;spf[i*q]=q;}}vector<pair<int,int>> cases={{364364,5},{114514,7},{114514,19},{114514,31},{114514,67},{114514,317}};
 for(auto[n,p]:cases){if(argc>2&&p!=stoi(argv[2]))continue;int D=(B-1)/p;int xmin=max(p+1,18);if(n==114514)xmin=p+1;for(int s:{-1,1}){auto ms=filters(n,p,s,primes);if(ms.size()>30)ms.resize(30);auto rs=roots(n,p,s,D,spf);ll candidates=0,passed=0;for(int d=1;d<=D;d++){int lower=max(xmin,p*d+1);for(int r:rs[d]){int x=lower+(r-lower%d+d)%d;for(;x<=B;x+=d){candidates++;bool ok=true;for(auto&m:ms)if(!m.ok[(ll)(d%m.q)*m.q+x%m.q]){ok=false;break;}if(!ok)continue;passed++;}}}cout<<n<<" p="<<p<<" sign="<<s<<" B="<<B<<" x_min="<<xmin<<" candidates="<<candidates<<" passed="<<passed<<" filters="<<ms.size()<<endl;}}
}
