## About
This is an arbitrary-precision-integer calculator made in C++ (a language that doesn't have native support for it)

## Compile the project
`g++ calculator.cpp -o calculator`

## Run the app
`./calculator <first big number> <operator> <second big number>` <br/>
The above command opens a REPL where you can enter expressions and get your responses back

## Reservations
- Doesn't work with decimal places as at now
- The validations for the string used to create the BigInt or for validating the expression is not very strong. For the large part, I expect one to input an expression that makes sense mathematically. Writing expressions 
such as `10.2.3 - 10` might throw off the app
- I am initializing the BigInt using `string` type obtained from the terminal. It's size is typically 32 bytes, which limits our calculation. That said, the BigInt is stored as a `vector<int>` which can hold arbitrarily big number consistent with the kind of calculations to be done with the calculator
- On iterating through the string, I am using `int` which, like string, is limited
- I am using `int` to save the position of the decimal. Assuming this is a very huge number that can't be held in an int variable, `vector<int>` is more appropriate
