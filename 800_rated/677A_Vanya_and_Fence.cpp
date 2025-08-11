#include <bits/stdc++.h>
using namespace std;

int main() {
    int n; int h; int op = 0;
    cin >> n >> h;
    for (int i = 0; i < n; i++) {
        int ind_height;
        cin >> ind_height;
        if (ind_height > h) {
            op += 2;
        }
        else op += 1;
    }
    cout << op;
    return 0;
}