#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    int zero_count = 0;
    int one_count = 0;
    cin >> s;
    for (int i = 0; i < s.length(); i++) {
        // cout << s[i] << endl;
        if (s[i] == '0') {
            one_count = 0;
            zero_count++;
        }
        else {
            zero_count = 0;
            one_count++;
        }
        if (zero_count >= 7 || one_count >= 7) {
            cout << "YES";
            break;
        }
    }
    if (zero_count < 7 && one_count < 7) cout << "NO";
    return 0;
}