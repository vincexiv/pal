#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <sstream>
#include <stdexcept>
#include <stack>



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

    // Constructor to be initialized with a boolean
    BigInt(const bool num) {
        if(num){
            digits.push_back(1);
        } else {
            digits.push_back(0);
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

    // Comparison (<=)
    bool operator<=(const BigInt& other) const {
        if (digits.size() < other.digits.size()) return true;
        if (digits.size() > other.digits.size()) return false;
        for (int i = digits.size() - 1; i >= 0; --i) {
            if (digits[i] < other.digits[i]) return true;
            if (digits[i] > other.digits[i]) return false;
        }
        return true;
    }

    // Comparison (==)
    bool operator==(const BigInt& other) const {
        if (digits.size() > other.digits.size()) return false;
        if (digits.size() < other.digits.size()) return false;
        for (int i = digits.size() - 1; i >= 0; --i) {
            if (digits[i] > other.digits[i]) return false;
            if (digits[i] < other.digits[i]) return false;
        }
        return true;
    }

   // Overloaded modulo operator
    BigInt operator%(const BigInt& other) const {
        if (other == BigInt("0")) {
            throw std::runtime_error("Modulo by zero");
        }

        BigInt dividend = *this;
        BigInt divisor = other;

        while (dividend >= divisor) {
            dividend = dividend - divisor;
        }

        return dividend;
    }

    // Power operator
    BigInt operator^(const BigInt& exponent) const {
        BigInt result("1");
        BigInt base = *this;
        BigInt exp = exponent;

        while (exp > BigInt("0")) {
            if ((exp % BigInt("2")) == BigInt("1")) {
                result = result * base;
            }
            base = base * base;
            exp = exp / BigInt("2");
        }

        return result;
    }

    // Overloaded comparison operators
    bool operator<(const BigInt& other) const {
        if (digits.size() != other.digits.size()) {
            return digits.size() < other.digits.size();
        }

        for (auto it1 = digits.rbegin(), it2 = other.digits.rbegin(); it1 != digits.rend(); ++it1, ++it2) {
            if (*it1 != *it2) {
                return *it1 < *it2;
            }
        }

        return false;
    }

    // Overloaded comparison operators
    bool operator>(const BigInt& other) const {
        if (digits.size() != other.digits.size()) {
            return digits.size() > other.digits.size();
        }

        for (auto it1 = digits.rbegin(), it2 = other.digits.rbegin(); it1 != digits.rend(); ++it1, ++it2) {
            if (*it1 != *it2) {
                return *it1 > *it2;
            }
        }

        return false;
    }
};

// Tokenize the input string into operands and operators
std::vector<std::string> tokenize(const std::string& expression) {
    std::vector<std::string> tokens;
    std::string _operand;
    std::string _operator;

    for (char ch : expression) {
        if (isdigit(ch)) {
            _operand += ch;
            if (!_operator.empty()) {
                tokens.push_back(_operator);
                _operator.clear();
            }
        } else {
            if (!_operand.empty()) {
                tokens.push_back(_operand);
                _operand.clear();
            }
            if (!isspace(ch)) {
                _operator += ch;
            }
        }
    }
    if (!_operand.empty()) {
        tokens.push_back(_operand);
    }

    return tokens;
}

// Convert infix to postfix using the Shunting-yard algorithm
std::vector<std::string> infixToPostfix(const std::vector<std::string>& tokens) {
    std::vector<std::string> output;
    std::stack<std::string> operators;

    auto precedence = [](const std::string& op) {
        if (op == "^") return 3;
        if (op == "*" || op == "/" || op == "%") return 2;
        if (op == "+" || op == "-") return 1;
        return 0;
    };

    auto isOperator = [](const std::string& token) {
        return token == "+" || token == "-" || token == "*" || token == "/" || token == "%" || token == "^";
    };

    for (const std::string& token : tokens) {
        if (isdigit(token[0])) {
            output.push_back(token);
        } else if (isOperator(token)) {
            while (!operators.empty() && precedence(operators.top()) >= precedence(token)) {
                output.push_back(operators.top());
                operators.pop();
            }
            operators.push(token);
        } else if (token == "(") {
            operators.push(token);
        } else if (token == ")") {
            while (!operators.empty() && operators.top() != "(") {
                output.push_back(operators.top());
                operators.pop();
            }
            operators.pop();
        }
    }

    while (!operators.empty()) {
        output.push_back(operators.top());
        operators.pop();
    }

    return output;
}


// Evaluate a postfix expression
BigInt evaluatePostfix(const std::vector<std::string>& postfix) {
    std::stack<BigInt> stack;

    for (const std::string& token : postfix) {
        if (isdigit(token[0])) {
            stack.push(BigInt(token));
        } else {
            BigInt b = stack.top(); stack.pop();
            BigInt a = stack.top(); stack.pop();

            if (token == "+") {
                stack.push(a + b);
            } else if (token == "-") {
                stack.push(a - b);
            } else if (token == "*") {
                stack.push(a * b);
            } else if (token == "/") {
                stack.push(a / b);
            } else if (token == "%") {
                stack.push(a % b);
            } else if (token == "^") {
                stack.push(a ^ b);
            }
        }
    }

    return stack.top();
}


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

        bool greater = input.find(">") != std::string::npos;
        bool less = input.find("<") != std::string::npos;
        bool equal = input.find("=") != std::string::npos;
        bool doingComparison =  greater || less || equal;

        if(doingComparison){
            // Parse the input into arguments
            std::istringstream iss(input);
            std::vector<std::string> args = tokenize(input);

            BigInt num1(args[0]);
            BigInt num2(args[2]);
            std::string op = args[1];

            if (op == ">=") {
                bool result = num1 >= num2;
                std::cout << result << std::endl;
            } else if (op == "<=") {
                bool result = num1 <= num2;
                std::cout << result << std::endl;
            } else if (op == ">") {
                bool result = num1 > num2;
                std::cout << result << std::endl;
            } else if (op == "<") {
                bool result = num1 < num2;
                std::cout << result << std::endl;
            } else if (op == "==") {
                bool result = num1 == num2;
                std::cout << result << std::endl;
            }
            continue;
        }

        std::vector<std::string> tokens = tokenize(input);
        std::vector<std::string> postfix = infixToPostfix(tokens);
        BigInt result = evaluatePostfix(postfix);
        std::cout << vectorToString(result.digits) << std::endl;
    }

    return 0;
}
