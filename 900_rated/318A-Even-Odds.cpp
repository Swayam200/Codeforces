#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n; long long k;
    cin >> n >> k;
    long long count_odds = (n + 1)/2;
    if (k <= count_odds) {
        // odd
        cout << 2*k - 1;
    }
    else {
        // even
        long long even_index = k - count_odds;
        cout << 2*even_index;
    }
    
    return 0;
}
