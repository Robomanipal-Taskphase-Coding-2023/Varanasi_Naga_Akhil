#include <iostream>

int euclideanGCD(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int num1, num2;
    
    std::cout << "Enter the first number: ";
    std::cin >> num1;

    std::cout << "Enter the second number: ";
    std::cin >> num2;

    int gcd = euclideanGCD(num1, num2);

    std::cout << "The GCD of " << num1 << " and " << num2 << " is " << gcd << std::endl;

    return 0;
}
