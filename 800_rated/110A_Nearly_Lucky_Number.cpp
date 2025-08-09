#include <iostream>
using namespace std;

int main() {
    long long n;
    int lucky_digit_count = 0;
    cin >> n;
    while (n > 0) {
        if ((n % 10 == 4) || (n % 10 == 7)) lucky_digit_count++;
        n /= 10;
    }
    if (lucky_digit_count == 4 || lucky_digit_count == 7)
    cout << "YES";
    else cout << "NO";
    return 0;
}