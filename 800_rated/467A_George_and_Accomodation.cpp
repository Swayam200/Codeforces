#include <iostream>
using namespace std;

int main() {
    int n; int p; int q;
    cin >> n;
    int count = 0;
    for (int i = 0; i < n; i++) {
        cin >> p >> q;
        if (p + 2 <= q) count++;
    }
    cout << count;
    return 0;
}