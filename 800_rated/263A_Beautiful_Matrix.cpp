#include <iostream>
#include <array>
using namespace std;

int main() {
    int row_pos; int col_pos;
    int arr[5][5] = {0};
    for (int i = 0; i < 5; i++) {
        for (int j = 0; j < 5; j++) {
            cin >> arr[i][j];
            if (arr[i][j] == 1) {
                row_pos = i; col_pos = j;   
            }
        }
    }
    int distance_from_centre_col = abs(2 - col_pos);
    int distance_from_centre_row = abs(2 - row_pos);
    cout << distance_from_centre_row + distance_from_centre_col;
    return 0;
}