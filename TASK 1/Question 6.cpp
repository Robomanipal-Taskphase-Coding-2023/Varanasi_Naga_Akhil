#include <iostream>
#include <vector>

using namespace std;


void bubbleSort(vector<int> &arr)
{
    int n = arr.size();
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}


void selectionSort(vector<int> &arr)
{
    int n = arr.size();
    for (int i = 0; i < n - 1; i++)
    {
        int min_index = i;
        for (int j = i + 1; j < n; j++)
        {
            if (arr[j] < arr[min_index])
            {
                min_index = j;
            }
        }
        if (min_index != i)
        {
            swap(arr[i], arr[min_index]);
        }
    }
}


int binarySearch(const vector<int> &arr, int target)
{
    int left = 0;
    int right = arr.size() - 1;
    while (left <= right)
    {
        int mid = left + (right - left) / 2;
        if (arr[mid] == target)
        {
            return mid;
        }
        else if (arr[mid] < target)
        {
            left = mid + 1;
        }
        else
        {
            right = mid - 1;
        }
    }
    return -1; 
}

int main()
{
    int n;
    cout << "Enter the number of elements: ";
    cin >> n;

    vector<int> arr(n);

    cout << "Enter " << n << " elements: ";
    for (int i = 0; i < n; i++)
    {
        cin >> arr[i];
    }

    char choice;
    cout << "Enter 's' for Selection Sort or 'b' for Bubble Sort: ";
    cin >> choice;

    if (choice == 's')
    {
        selectionSort(arr);
        cout << "Sorted array using Selection Sort: ";
    }
    else if (choice == 'b')
    {
        bubbleSort(arr);
        cout << "Sorted array using Bubble Sort: ";
    }
    else
    {
        cout << "Invalid choice. Exiting..." << endl;
        return 1;
    }

    for (int i = 0; i < n; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;

    int target;
    cout << "Enter the number to search: ";
    cin >> target;

    int result = binarySearch(arr, target);
    if (result != -1)
    {
        cout << "Element found at position " << result << endl;
    }
    else
    {
        cout << "Element not found in the array." << endl;
    }

    return 0;
}
