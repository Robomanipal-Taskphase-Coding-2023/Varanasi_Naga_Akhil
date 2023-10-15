#include <iostream>

int sumOfDigitsWithoutRecursion(int number) {
    int sum = 0;
    while (number > 0) {
        sum += number % 10; 
        number /= 10; 
    }
    return sum;
}

int main() {
    int number;
    
    std::cout << "Enter a positive integer: ";
    std::cin >> number;

    if (number < 0) {
        std::cout << "Please enter a positive integer." << std::endl;
    } else {
        int result = sumOfDigitsWithoutRecursion(number);
        std::cout << "Sum of digits: " << result << std::endl;
    }

    return 0;
}
