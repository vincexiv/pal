# Compile
`g++ calculator.cpp -o calculator`

# Run the app in REPL
`./calculator <first big number> <operator> <second big number>` <br/>
Enter your expressions

# Reservations
- only works with positive integers no floating point, or negative stuff for now
- The validations for the string used to create the BigInt or for validating the expression is not very strong. For the large part, I expect one to input an expression that makes sense mathematically. Writing expressions 
such as `10 -- 3` might throw off the app
- I used `size_t` when iterating through the string used to create BigInt. Apparently, it is 
limited. In 32 bit systems, it is a 32 bit unsigned integer, while in 64 bit systems, it is 
64 bit unsigned integer. I was expecting something unlimited
