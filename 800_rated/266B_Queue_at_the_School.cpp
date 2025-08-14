#include <bits/stdc++.h>
using namespace std;

int main() {
    int n; int t; string s; string new_s;
    cin >> n >> t >> s;
    new_s = s;
    while (t--) {
        for (int i = 0; i < n; i++) {
            if (s[i] == 'B') {
                if (s[i + 1] == 'G') {
                    swap(new_s[i], new_s[i + 1]);
                }
            }
        }
        s = new_s;
    }
    cout << new_s;
    return 0;
}