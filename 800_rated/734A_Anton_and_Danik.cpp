#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    string game;
    cin >> game;
    int anton_win_count = 0;
    int danik_win_count = 0;
    for (int i = 0; i < n; i++) {
        if (game[i] == 'A')
            anton_win_count++;
        else
            danik_win_count++;
    }
    if (anton_win_count > danik_win_count)
        cout << "Anton";
    else if (anton_win_count == danik_win_count)
        cout << "Friendship";
    else
        cout << "Danik";
    return 0;
}