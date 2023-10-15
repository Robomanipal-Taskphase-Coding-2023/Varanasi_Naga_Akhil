#include <iostream>
#include <cstring>
void bubbleSort(char arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                char temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}
 
int main() {
    char arr[] = "worksheet";
    int n = strlen(arr);

    std::cout << "Original Array: " << arr << std::endl;

    bubbleSort(arr, n);

    std::cout << "Sorted Array: " << arr << std::endl;

    return 0;
}
