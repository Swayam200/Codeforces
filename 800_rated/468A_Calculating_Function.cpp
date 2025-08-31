#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    cin >> n;
    int sum = 0;
    if (n % 2 == 0) cout << n/2;
    else {
        cout << n/2 - n;
    }
    return 0;
}