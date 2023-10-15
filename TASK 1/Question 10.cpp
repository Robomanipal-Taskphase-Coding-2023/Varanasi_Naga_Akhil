#include <iostream>


unsigned long long fibonacci(int n)
{
    if (n <= 1)
    {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main()
{
    int n = 41; 

    std::cout << "Calculating the first " << n << " Fibonacci numbers:" << std::endl;

    for (int i = 0; i < n; ++i)
    {
        std::cout << "F(" << i << ") = " << fibonacci(i) << std::endl;
    }

    return 0;
}
 