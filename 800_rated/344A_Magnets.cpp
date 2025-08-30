#include <bits/stdc++.h>
using namespace std;

int main() {
    int n; int segments = 0; string s;
    cin >> n;
    char first; char second;
    for (int i = 0; i < n; i++) {
        cin >> first >> second;
        s += first;
        s += second;
    }
    // cout << s << endl;

    for (int i = 0; i < s.size(); i++) {
        if (s[i] == s[i + 1]) segments++;
    }
    cout << segments + 1;
    return 0;
}