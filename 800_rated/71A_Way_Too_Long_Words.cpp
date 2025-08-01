#include <iostream>
#include <string>
#include <vector>
using namespace std;

void problem(vector<string> k) {
    for (auto it : k) {
        if (it.size() <= 10)
        {
            cout << it << endl;
        }
        else
        {
            string new_string;
            int count = 0;
            for (int i = 1; i < it.length() - 1; i++)
            {
                count++;
            }
            cout << string(it.front() + to_string(count) + it.back()) << endl;
        }
    }
}

int main() {
    int n;
    string k;
    cin >> n;
    vector<string> input;
    for(int i = 0; i < n; i++) {
        cin >> k;
        input.emplace_back(k);
    }
    problem(input);
    return 0;
}