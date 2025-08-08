#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main()
{
    string s;
    cin >> s;
    int lower_words_count = 0;
    int upper_words_count = 0;
    for (int i = 0; i < s.size(); i++)
    {
        if (islower(s[i]))
            lower_words_count++;
        else
            upper_words_count++;
    }
    for (auto it : s)
    {
        if (lower_words_count < upper_words_count)
        {
            cout << char(toupper(it));
        }
        else
        {
            cout << char(tolower(it));
        }
    }
    return 0;
}