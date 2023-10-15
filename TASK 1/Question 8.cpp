#include <iostream>
#include <vector>

using namespace std;


vector<vector<int>> matrixMultiplication(const vector<vector<int>>& A, const vector<vector<int>>& B) {
    int numRowsA = A.size();
    int numColsA = A[0].size();
    int numRowsB = B.size();
    int numColsB = B[0].size();

    
    if (numColsA != numRowsB) {
        cout << "Matrix multiplication is not possible. Columns of A must be equal to rows of B." << endl;
        return vector<vector<int>>();
    }

    
    vector<vector<int>> result(numRowsA, vector<int>(numColsB, 0));

    
    for (int i = 0; i < numRowsA; i++) {
        for (int j = 0; j < numColsB; j++) {
            for (int k = 0; k < numColsA; k++) {
                result[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    return result;
}


vector<vector<int>> transposeMatrix(const vector<vector<int>>& matrix) {
    int numRows = matrix.size();
    int numCols = matrix[0].size();

    
    vector<vector<int>> transpose(numCols, vector<int>(numRows, 0));

    
    for (int i = 0; i < numRows; i++) {
        for (int j = 0; j < numCols; j++) {
            transpose[j][i] = matrix[i][j];
        }
    }

    return transpose;
}

int main() {
    vector<vector<int>> A = {{1, 2, 3},
                              {4, 5, 6}};

    vector<vector<int>> B = {{7, 8},
                              {9, 10},
                              {11, 12}};

    
    vector<vector<int>> result = matrixMultiplication(A, B);

    cout << "Matrix A:" << endl;
    for (const auto& row : A) {
        for (int element : row) {
            cout << element << " ";
        }
        cout << endl;
    }

    cout << "Matrix B:" << endl;
    for (const auto& row : B) {
        for (int element : row) {
            cout << element << " ";
        }
        cout << endl;
    }

    cout << "Result of A * B:" << endl;
    for (const auto& row : result) {
        for (int element : row) {
            cout << element << " ";
        }
        cout << endl;
    }

   
    vector<vector<int>> transposeA = transposeMatrix(A);

    cout << "Transpose of Matrix A:" << endl;
    for (const auto& row : transposeA) {
        for (int element : row) {
            cout << element << " ";
        }
        cout << endl;
    }

    return 0;
}
