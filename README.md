# Simple Calculator - (Flask app deployed on Vercel)
This is my first Python webapp. It uses Flask and is deployed on Vercel: [https://fcalc.vercel.app/](https://fcalc.vercel.app/)

A calculator of this scale (basic operations + bracketing) would definitely not need a server backend. And a calculator is part of any OSs anyway (breaking news: soon available even in iPads - [MacRumours article 23/04/2024](https://www.macrumors.com/2024/04/23/calculator-app-for-ipad-rumor/) ). The application is rather a showcase for a simple application one grade more complicated than the usual "Hello World" examples.

# Usage
## 'Normal' usage
As expected, e.g. in order to compute `3.2 + 5.8` one should push the following buttons in order:
* `3`
* `.` _(decimal separator)_
* `2`
* `+` _(at this point the actual 3.2 and the '+' sign are forwarded to the backend - see below)_
* `5`
* `.`
* `8` _(nothing happens since the Frontend has no idea if You would or would not go on with other decimals / operators etc.)_
* `=` _(now the Frontend finally understands You've finished, so the actual 5.8 gets dispatched to the Backend)_
* backend evaluates `3.2 + 5.8` to `9` and sends it back to the frontend

The _usual_ operator precedence is applied, e.g. `3.2 + 5.8 * 2` gets evaluated as `3.2 + 5.8 * 2 == 3.2 + 11.6 == 14.8`.

## Take a function of the actual result
Suppose we entered `3.2 + 5.8` making `9` but in reality we wanted to take the square root of the sum. Instead of clearing up (`CLR`) and entering the formula correctly by starting with the function:
* simply push the `square root` button
* the `SQRT` operator gets dispatched to the backend
* backend detects `3.2 + 5.8 SQRT` would lead to an erroneous formula. But since `SQRT` was a function, user intention may have been to calculate `SQRT(3.2 + 5.8)`
* actual formula (`3.2 + 5.8 SQRT`) gets replaced to `SQRT(3.2 + 5.8)`, gets evaluated and the result sent back to the Frontend
* Frontend shows 3 as a result (since `SQRT(3.2+5.8) == SQRT(9) == 3`

## Bracket the actual result
Suppose we entered `3.2 + 5.8` making `9` but in reality we wanted to multiply this sum by 2:
* simply push the `)` _(closing bracket)_ button
* the `)` gets dispatched to the backend
* backend detects the previous formula (`3.2 + 5.8`) was correct but adding a closing bracket does not make sense (`3.2 + 5.8 )`). So the entire previous formula should be bracketed instead
* previous formula `3.2 + 5.8` gets replaced with `(3.2 + 5.8)` and sent back to the Frontend
* Frontend shows 9 as a result (since `(3.2+5.8) == (9) == 9`
* now we can proceed with the multiplication: push
  * `*`
  * `2`
  * `=`
* result should be 18...

# Architecture
## Frontend
HTML + Bootstrap
JS script handles 
* user inputs: Number button + decimal separator -> collects Number Literal as long as another button is pushed
  * correctness of the actual number literal is checked in the browser, e.g. a number can contain up to one decimal separator...
* AJAX calls: whenever an operator / bracket / equal sign is pushed, the actual number literal plus the operator is sent to the Server side
* returning data: actual state (e.g. imbalanced bracketing detected) + actual result (when available) + enabled/disabled buttons + page refresh according to all these info

## Backend
Flask App following the Application Factory Pattern.
In one cycle:
* the incoming POST messages contain the actual number literal (shown on the screen) + an operator label (operator / bracket / equal sign)
* these get appended to the actual formula (stored as a list)
* an attempt is made to evaluate the actual formula (convert to polish form + evaluation)
* bracket signs are collected in a different stack as well in order to see if the actual formula is properly bracketed or not
* decision on which buttons to enable / disable
  * e.g. `3 + * 2` would not make sense, so when the actual formula is `3 +` all the operators  + the closing bracket gets disabled
  * `3 +` may be followed by a number literal / an opening bracket / a function, so these (and only these) are enabled
  * if user wanted to add e.g. `-2` then it should be bracketed: `3 + ( - 2)`
* send back state (formula is complete / incomplete, proper result is available), actual result, enabled/disabled button labels to the Frontend

## Vercel specificities
Since Python is not as native to Vercel as e.g. NodeJS, there is no available deployement framework. So "Other" must have been chosen.
The key to success lies in `vercel.json` which would tell Vercel
* to build the whole thing using its own Python
* and handle all incoming requests with `run.py`

The environmental variables `FLASK_ENV` and `FLASK_SECRET_KEY` would tell the app if this is a production environment or not.
