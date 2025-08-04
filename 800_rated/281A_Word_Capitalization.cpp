#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string word;
    string first_letter;
    cin >> word;
    first_letter = toupper(char(word[0]));
    cout << first_letter;
    for (int i = 1; i < word.length(); i++) {
        cout << word[i];
    }
    return 0;
}