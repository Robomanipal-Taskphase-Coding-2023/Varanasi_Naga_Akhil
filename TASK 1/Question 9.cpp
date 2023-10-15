#include <iostream>
#include <string>
#include <algorithm>
void charlen(string str[], int n)
{
    
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (str[j].length() > str[j + 1].length())
            {
                
                string temp = str[j];
                str[j] = str[j + 1];
                str[j + 1] = temp;
            }
        }
    }
}
void sort(string str[], int n){

}

int main()
{
    
    string str[] = {"cat","word","number"};
    int n = sizeof(str) / sizeof(str[0]);

    
    charlen(str, n);

    
    for (int i = 0; i < n; i++)
    {
        std::cout << str[i] << " ";
    }
    std::cout << std::endl;
    
    for (int i = 0; i < n; i++){
        std::sort(str.begin(), str.end());
        std::cout << "Sorted string: " << str << std::endl;
    }
        return 0;
}
