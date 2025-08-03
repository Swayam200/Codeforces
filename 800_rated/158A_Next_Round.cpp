#include <iostream>
using namespace std;

int main() {
    int arr[50] = {0};
    int n;
    int k_th_position;
    int scores;
    int count = 0;
    cin >> n >> k_th_position;
    for (int i = 0; i < n; i++) {
        cin >> scores;
        arr[i] = scores;
    }
    for (auto it : arr) {
        if ((it >= arr[k_th_position - 1]) && (it > 0)) count++;
    }
    cout << count << " ";
    return 0;
}
