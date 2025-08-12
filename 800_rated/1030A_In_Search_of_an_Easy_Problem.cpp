#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    int q;
    for (int i = 0; i < n; i++) {
        cin >> q;
        if (q == 1) {
            cout << "HARD"; break;
        }
    }
    if (q != 1) cout << "EASY";
    return 0;
}