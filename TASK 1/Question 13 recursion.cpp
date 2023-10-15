#include <iostream>

int sumOfDigitsWithRecursion(int number) {
    if (number == 0) {
        return 0; 
    } else {
        return number % 10 + sumOfDigitsWithRecursion(number / 10); 
    }
}

int main() {
    int number;
    
    std::cout << "Enter a positive integer: ";
    std::cin >> number;

    if (number < 0) {
        std::cout << "Please enter a positive integer." << std::endl;
    } else {
        int result = sumOfDigitsWithRecursion(number);
        std::cout << "Sum of digits: " << result << std::endl;
    }

    return 0;
}
