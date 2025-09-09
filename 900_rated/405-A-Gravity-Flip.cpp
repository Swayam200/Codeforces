#include <bits/stdc++.h>
using namespace std;

int main() {
    int n; int val;
    cin >> n;
    vector<int> v;
    for (int i = 0; i < n; i++) {
        cin >> val;
        v.emplace_back(val);
    }
    sort(v.begin(), v.end());
    for (auto it : v) {
        cout << it << " ";
    }
    return 0;
}