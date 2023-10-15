#include <iostream>
#include <cstring>
void copyString(char *dest, const char *src) {
    while (*src != '\0') {
        *dest = *src;
        src++;
        dest++;
    }
    *dest = '\0';
}
int main() {
    char source[100];
    char destination[100];
    std::cout << "Enter a string: ";
    std::cin.getline(source, sizeof(source));
    copyString(destination, source);
    std::cout << "Source: " << source << std::endl;
    std::cout << "Destination: " << destination << std::endl;
    return 0;
}
