#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    int entry; int exit; int current_passengers = 0; int max_passengers = 0;
    for (int i = 0; i < n; i++) {
        cin >> exit >> entry;
        current_passengers -= exit;
        current_passengers += entry;
        max_passengers = max(max_passengers, current_passengers);
    }
    cout << max_passengers;
    return 0;
}