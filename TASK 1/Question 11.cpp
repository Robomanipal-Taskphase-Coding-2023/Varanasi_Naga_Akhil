#include <iostream>
#include <vector>

int binarySearch(const std::vector<int>& arr, int target, int left, int right) {
    if (left > right) return -1;

    int mid = (left + right) / 2;
    if (arr[mid] == target) return mid;
    return (arr[mid] > target) ? binarySearch(arr, target, left, mid - 1) : binarySearch(arr, target, mid + 1, right);
}

int main() {
    std::vector<int> arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int target = 7;
    int result = binarySearch(arr, target, 0, arr.size() - 1);

    if (result != -1) std::cout << "Element " << target << " found at index " << result << std::endl;
    else std::cout << "Element " << target << " not found in the array." << std::endl;

    return 0;
}
