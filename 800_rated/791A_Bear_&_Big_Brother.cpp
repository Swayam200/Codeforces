#include <iostream>
using namespace std;

int main() {
    int a; int b; int count = 0;
    cin >> a >> b;
    do {
        a *= 3;
        b *= 2;
        count++;
        // cout << "a: " << a << " , b: " << b << " , count: " << count << endl;
    } while (a <= b);
    cout << count;  
    return 0;
}