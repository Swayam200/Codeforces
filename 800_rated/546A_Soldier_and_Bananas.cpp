#include <iostream>
using namespace std;

int main() {
    int k; int n; int w;
    cin >> k >> n >> w;
    int total_cost = 0;
    for (int i = 1; i <= w; i++) {
        total_cost = total_cost + (i * k);
    }
    int output = total_cost - n;
    if (output < 0) cout << 0;
    else cout << output;
    return 0;
}