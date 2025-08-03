#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    string operation;
    string start;
    string end;
    int count = 0;
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> operation;
        start = operation.at(0);
        end = operation.at(2);
        if (start == "+" || end == "+") count++;
        else count--;
    }
    cout << count;
    return 0;
}