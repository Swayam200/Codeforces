#include <bits/stdc++.h>
using namespace std;

int main() {
    int n; int val; int min = INT_MAX; int count = 1; priority_queue<int> find_max_count;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> val;
        if (val < min) {
            min = val;
            count = 1;
        }
        else {
            min = val;
            count++;
        }
        find_max_count.push(count);
    }
    cout << find_max_count.top();
    return 0;
}