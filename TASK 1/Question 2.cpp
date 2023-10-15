#include <iostream>

int main() {
    int matrix1[10][10], matrix2[10][10], result[10][10];
    int rows1, cols1, rows2, cols2;

    
    std::cout << "Enter the number of rows and columns for matrix1: ";
    std::cin >> rows1 >> cols1;
    std::cout << "Enter the elements of matrix1:\n";
    for (int i = 0; i < rows1; ++i)
        for (int j = 0; j < cols1; ++j)
            std::cin >> matrix1[i][j];

   
    std::cout << "Enter the number of rows and columns for matrix2: ";
    std::cin >> rows2 >> cols2;
    std::cout << "Enter the elements of matrix2:\n";
    for (int i = 0; i < rows2; ++i)
        for (int j = 0; j < cols2; ++j)
            std::cin >> matrix2[i][j];

   
    if (cols1 != rows2) {
        std::cout << "the entered matrices are not compatible.\n";
        return 1;
    }

    
    for (int i = 0; i < rows1; ++i) {
        for (int j = 0; j < cols2; ++j) {
            result[i][j] = 0;
            for (int k = 0; k < cols1; ++k) {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }

    
    std::cout << "Product matrix:\n";
    for (int i = 0; i < rows1; ++i) {
        for (int j = 0; j < cols2; ++j) {
            std::cout << result[i][j] << " ";
        }
        std::cout << "\n";
    }

    return 0;
}
