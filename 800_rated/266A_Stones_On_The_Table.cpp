#include <iostream>
#include <list>
#include <string>
using namespace std;

int main() {
    int n; string s; int count = 0;
    cin >> n >> s;
    for (int i = 0; i < n; i++) {
        if (s[i] == s[i - 1]) count++;
    }
    cout << count;
    return 0;
}