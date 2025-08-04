#include <iostream>
#include <set>
#include <string>
using namespace std;

int main() {
    string user_name;
    set<char> s;
    cin >> user_name;
    for (int i = 0; i < user_name.length(); i++) {
        s.insert(user_name[i]);
    }
    int unique_char = s.size();
    if (unique_char % 2 == 0) cout << "CHAT WITH HER!";
    else cout << "IGNORE HIM!";
    return 0;
}