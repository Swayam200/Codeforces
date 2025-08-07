#include <iostream>
using namespace std;

int main() {
    int x;
    cin >> x;
    int count = 0;
    int i = 5;
    while (x > 0) {
        if ((x - i) >= 0) {
            x -= i;
            count++;
        }
        else i--;
    }
    cout << count;
    return 0;
}