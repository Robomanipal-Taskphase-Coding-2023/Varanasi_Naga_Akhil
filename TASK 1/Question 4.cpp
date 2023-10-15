#include <iostream>
using namespace std;


bool isHillNumber(int n)
{
	int prevDigit = -1;
	bool ascending = true;

	while (n > 0)
	{
		int digit = n % 10;
		n /= 10;

		if (digit == prevDigit)
		{
			return false; 
		}

		if (ascending)
		{
			if (digit < prevDigit)
			{
				ascending = false;
			}
		}
		else
		{
			if (digit > prevDigit)
			{
				return false; 
			}
		}

		prevDigit = digit;
	}

	return !ascending; 
}

int main()
{
	int num;
	cout << "Enter a number: ";
	cin >> num;

	if (isHillNumber(num))
	{
		cout << "Hill Number: " << num << endl;
	}
	else
	{
		cout << "Not Hill Number: " << num << endl;
	}

	return 0;
}
