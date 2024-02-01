#include<iostream>
#include<chrono>
#include<random>
#include<fstream>

using namespace std;
mt19937 rnd(chrono::steady_clock::now().time_since_epoch().count());
using pii = pair<int, int>;
#define f first
#define s second

void solve() {
    int n = 9'999, h = 20;
    vector<pair<pii, pii>> ans;
    for (int i = 0; i < n; ++i) {
        int l1 = 0, r1, l2, r2 = 800;
        int k = rnd() % (800 - 2 * h);
        r1 = k;
        l2 = r1 + 2 * h;
        cout << l1 << ' ' << r1 << '\n' << l2 << ' ' << r2 << '\n';
    }
    cout << endl;
}

signed main() {
//    ios_base::sync_with_stdio(false);
//    cin.tie(nullptr);
//    cout.tie(nullptr);
    freopen("gen_res.txt", "w", stdout);
    int T = 1;
    while (T--) {
        solve();
    }
    return 0;
}