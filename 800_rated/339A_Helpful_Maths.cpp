#include <iostream>
#include <string>
#include <list>
using namespace std;

int main() {
    string s;
    string answer;
    int positive_counter = 0;
    list<int> l;
    cin >> s;
    for (int i = 0; i < s.length(); i++) {
        if (s[i] == '+') positive_counter++;
        else {
            int numbers = s[i] - '0';
            l.emplace_back(numbers);
        }
    }
    l.sort();
    for (auto it : l) {
        answer.append(to_string(it));
        // cout << it;
        if (positive_counter > 0) {
            // cout << "+";
            answer.append("+");
            positive_counter--;
        }
    }
    cout << answer << endl;
    return 0;
}