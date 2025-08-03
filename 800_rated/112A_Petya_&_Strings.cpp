#include <iostream>
#include <string>
#include <cctype>
using namespace std;

// if string same - 0
// if 1st string greater - 1
// if 2nd string greater - -1

int main() {
    string input_string1; string input_string2;
    char character1; char character2;
    string answer;
    cin >> input_string1 >> input_string2;
    
    for (int i = 0; i < input_string1.length(); i++) {
        character1 = tolower(input_string1[i]); 
        character2 = tolower(input_string2[i]);
        if (character1 == character2) {
            answer = "0";
        }
        else if (character1 > character2) {
            answer = "1";
            break;
        }
        else {
            answer = "-1";
            break;
        }
    }
    cout << answer;
    return 0;
}