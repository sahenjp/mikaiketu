#include <bits/stdc++.h>
using namespace std;using ll=long long;
#ifndef BASE_BOUND
#define BASE_BOUND 10000000
#endif
static_assert(BASE_BOUND>=1000000 && BASE_BOUND<=10000000);
int pw(ll a,int e,int q){ll r=1;for(;e;e>>=1,a=a*a%q)if(e&1)r=r*a%q;return r;}
vector<int> subgroup(int p,int k,int q){
 for(int a=2;a<q;a++){
   int g=pw(a,p,q); bool ok=true;int d=k;
   for(int t=2;t*t<=d;t++)if(d%t==0){if(pw(g,k/t,q)==1){ok=false;break;}while(d%t==0)d/=t;}
   if(ok&&d>1&&pw(g,k/d,q)==1)ok=false;
   if(!ok)continue;
   vector<int> v(k);v[0]=1;for(int i=1;i<k;i++)v[i]=(ll)v[i-1]*g%q;sort(v.begin(),v.end());return v;
 }
 abort();
}
int main(){const int P=BASE_BOUND,K=108,M=P*K+1;vector<bool>pr(M+1,true);pr[0]=pr[1]=false;for(int i=2;i*i<=M;i++)if(pr[i])for(int j=i*i;j<=M;j+=i)pr[j]=false;
 int cnt=0; vector<int> Ns={114514,364364};vector<vector<int>> rem(2);
 for(int p=5;p<=P;p++)if(pr[p]){cnt++;int mask=3;for(int k=2;k<=K&&mask;k+=2){int q=k*p+1;if(!pr[q])continue;auto s=subgroup(p,k,q);for(int i=0;i<2;i++)if(mask>>i&1){int n=Ns[i]%q;bool ok=false;for(int x:s){for(int y:s){int z=((ll)n-x-y+2LL*q)%q;if(z==0||binary_search(s.begin(),s.end(),z)){ok=true;break;}}if(ok)break;}if(!ok)mask^=1<<i;}}
 for(int i=0;i<2;i++)if(mask>>i&1)rem[i].push_back(p);}
 cout<<"prime count="<<cnt<<endl;for(int i=0;i<2;i++){cout<<Ns[i]<<":";for(int p:rem[i])cout<<" "<<p;cout<<endl;}}
