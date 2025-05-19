const fs = require('fs');

data = fs.readFileSync('stuff.txt', 'utf8');

let lines = data.split('\n');

function is_digit(input){
    let digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for (digit of digits){
        if (input[0] == digit){
            return true
        }
    }

    return false
}

// Must start with xx/xx where x is a digit
function starts_width_date(input){
    if (is_digit(input[0]) && is_digit(input[1]) && input[2] == '/' && is_digit(input[3]) && is_digit(input[4])){
        return true
    }

    return false
}

let result = []
let amounts = []
for (let i = 0; i < lines.length; i++) {
    line_output = ""

    // If the line starts with a date, we need to start a new line with the date, Citizen (for bank row), description (only keep the stuff after the "- "), then amount
    if (starts_width_date(lines[i])){
        // Add the amount for the previous line
        if (result.length > 0){
            result[result.length - 1] += ", " + amounts[amounts.length - 1]
        }

        // Start the new line
        line_split = lines[i].split(' ')

        amounts.push(line_split[1]) // Add the amount to the amounts array
        line_output = line_split[0] + ", Citizen, " // + description (may span multiple lines or spaces)

        line_output += line_split.slice(2).join(' ').split('- ')[1] // + description (may span multiple lines or spaces), Only keeps the stuff after the "- "

        result.push(line_output)
    }
    else {
        result[result.length - 1] += lines[i]
    }
}

// Add the amount for the last line
if (result.length > 0){
    result[result.length - 1] += ", " + amounts[amounts.length - 1]
}

// Remove \r characters
for (let i = 0; i < result.length; i++) {
    result[i] = result[i].replace(/\r/g, '')
}

console.log(result)

// Save to a text file
fs.writeFileSync('result.txt', result.join('\n'), 'utf8');