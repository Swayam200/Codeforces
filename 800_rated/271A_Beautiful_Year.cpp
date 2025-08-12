#include <bits/stdc++.h>
using namespace std;

int main() {
    int y; 
    cin >> y;
    y++;
    int distinct_count = 0; unordered_map<int, int> mpp; int sum;
    while (sum != 4) {
        int y_copy = y;
        for (int i = 0; i < 4; i++) {
            int digit = y_copy % 10;
            y_copy /= 10;
            if (mpp[digit] < 1) mpp[digit]++;
        }
        for (auto it : mpp) {
            sum += it.second;
        }
        // cout << y << " " << sum << endl;
        if (sum == 4)
            {cout << y; break;}
        y++;
        sum = 0;
        mpp.clear();
    }
    return 0;
}