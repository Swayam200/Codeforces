#include <iostream>
#include <string>
#include <stack>
using namespace std;

int main() {
    string s; string t; string rev = "";
    cin >> s >> t;
    stack<char> words;
    for (int i = 0; i < s.size(); i++) {
        words.push(s[i]);
    }
    for (int i = 0; i < s.size(); i++) {
        // cout << words.top();
        rev += words.top();
        words.pop();
    }
    if (rev != t)
        cout << "NO";
    else cout << "YES";
    return 0;
}