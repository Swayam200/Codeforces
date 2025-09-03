#include <bits/stdc++.h>
using namespace std;

int main() {
    int n; int twin_coin = 0; int q; int my_coin = 0;
    cin >> n; int index = 0; int count = 0;
    int arr[n];
    for (int i = 0; i < n; i++) {
        cin >> q;
        arr[i] = q;
        twin_coin += q;
    }
    sort(arr, arr + n, greater<int>());
    while (my_coin <= twin_coin) {
        my_coin += arr[index];
        twin_coin -= arr[index];
        index++;
        count++;
        // cout << my_coin << " " << twin_coin << " " << count << endl;
        if (index == n) {
            break;
        }
    }
    cout << count;
    return 0;
}