#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int decimalNumber;

    
    cout << "Enter a decimal number: ";
    cin >> decimalNumber;

    
    cout << "Hexadecimal: 0x" << hex << decimalNumber << endl;
    cout << "Octal: 0" << oct << decimalNumber << endl;
    cout << "Binary: ";
    
    int binary[32];
    int index = 0;

    
    while (decimalNumber > 0) {
        binary[index] = decimalNumber % 2;
        decimalNumber /= 2;
        index++;
    }

    
    for (int i = index - 1; i >= 0; i--) {
        cout << binary[i];
    }
    cout << endl;

    return 0;
}
