#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>


std::string vectorToString(const std::vector<int>& vec) {
    std::ostringstream oss;
    oss << "";
    for (size_t i = 0; i < vec.size(); ++i) {
        oss << vec[vec.size() - i - 1];
    }
    return oss.str();
}

class BigInt {
public:
    // Stores digits of the number in reverse order
    std::vector<int> digits;

    // Constructor to initialize BigInt from a string
    BigInt(const std::string& num) {
        for (int i = num.size() - 1; i >= 0; --i) {
            digits.push_back(num[i] - '0');
        }
    }

    // Constructor for zero BigInt
    BigInt() = default;

    // Print the number
    void print() const {
        if (digits.empty()) {
            std::cout << "0";
            return;
        }
        for (int i = digits.size() - 1; i >= 0; --i) {
            std::cout << digits[i];
        }
    }

    // Addition
    BigInt operator+(const BigInt& other) const {
        BigInt result;
        int carry = 0;
        size_t i = 0;
        while (i < digits.size() || i < other.digits.size() || carry) {
            int sum = carry;
            if (i < digits.size()) sum += digits[i];
            if (i < other.digits.size()) sum += other.digits[i];
            result.digits.push_back(sum % 10);
            carry = sum / 10;
            ++i;
        }
        return result;
    }

    // Subtraction
    BigInt operator-(const BigInt& other) const {
        BigInt result;
        int borrow = 0;
        size_t i = 0;
        while (i < digits.size() || i < other.digits.size()) {
            int diff = borrow;
            if (i < digits.size()) diff += digits[i];
            if (i < other.digits.size()) diff -= other.digits[i];
            if (diff < 0) {
                diff += 10;
                borrow = -1;
            } else {
                borrow = 0;
            }
            result.digits.push_back(diff);
            ++i;
        }

        // Remove leading zeros
        while (result.digits.size() > 1 && result.digits.back() == 0) {
            result.digits.pop_back();
        }

        return result;
    }

    // Multiplication
    BigInt operator*(const BigInt& other) const {
        BigInt result;
        result.digits.resize(digits.size() + other.digits.size(), 0);
        for (size_t i = 0; i < digits.size(); ++i) {
            for (size_t j = 0; j < other.digits.size(); ++j) {
                result.digits[i + j] += digits[i] * other.digits[j];
                result.digits[i + j + 1] += result.digits[i + j] / 10;
                result.digits[i + j] %= 10;
            }
        }

        // Remove leading zeros
        while (result.digits.size() > 1 && result.digits.back() == 0) {
            result.digits.pop_back();
        }

        return result;
    }

    // Division
    BigInt operator/(const BigInt& other) const {
        BigInt result, remainder;
        for (int i = digits.size() - 1; i >= 0; --i) {
            remainder.digits.insert(remainder.digits.begin(), digits[i]);
            int quotient = 0;
            while (remainder >= other) {
                remainder = remainder - other;
                quotient++;
            }
            result.digits.push_back(quotient);
        }

        // Reverse the result to correct the digit order
        std::reverse(result.digits.begin(), result.digits.end());

        // Remove leading zeros
        while (result.digits.size() > 1 && result.digits.back() == 0) {
            result.digits.pop_back();
        }

        return result;
    }

    // Comparison (>=)
    bool operator>=(const BigInt& other) const {
        if (digits.size() > other.digits.size()) return true;
        if (digits.size() < other.digits.size()) return false;
        for (int i = digits.size() - 1; i >= 0; --i) {
            if (digits[i] > other.digits[i]) return true;
            if (digits[i] < other.digits[i]) return false;
        }
        return true;
    }
};


int main() {
    std::string input;

    std::cout << "Welcome to the C++ REPL! Enter arguments separated by spaces (type 'exit' to quit):\n";

    while (true) {
        // Prompt for input
        std::cout << "> ";
        std::getline(std::cin, input);

        // Check for exit condition
        if (input == "exit") {
            std::cout << "Goodbye!\n";
            break;
        }

        // Parse the input into arguments
        std::istringstream iss(input);
        std::vector<std::string> args;
        std::string arg;

        while (iss >> arg) {
            args.push_back(arg);
        }

        BigInt num1(args[0]);
        BigInt num2(args[2]);
        char op = args[1][0];

        BigInt bigIntResult;
        std::string result;

        switch (op) {
            case '+':
                bigIntResult = num1 + num2;
                result = vectorToString(bigIntResult.digits);
                break;
            case '-':
                bigIntResult = num1 - num2;
                result = vectorToString(bigIntResult.digits);
                break;
            case '/':
                bigIntResult = num1 / num2;
                result = vectorToString(bigIntResult.digits);
                break;
            case '*':
                bigIntResult = num1 * num2;
                result = vectorToString(bigIntResult.digits);
                break;
            default:
                break;
        }

        std::cout << result << std::endl;
    }

    return 0;
}
