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
for (let i = 0; i < lines.length; i++) {
    line_output = ""

    // If the line starts with a date, we need to start a new line with the date, Citizen (for bank row), amount, then description (only keep the stuff after the "- ")
    if (starts_width_date(lines[i])){
        line_split = lines[i].split(' ')
        line_output = line_split[0] + ", Citizen, " + line_split[1] + ", " // + description (may span multiple lines or spaces)
        // for(i = 2; i < line_split.length; i++){
        //     line_output += line_split[i] + " "
        // }
        line_output += line_split.slice(2).join(' ').split('- ')[1] // + description (may span multiple lines or spaces), Only keeps the stuff after the "- "

        result.push(line_output)
    }
    else {
        result[result.length - 1] += lines[i]
    }
}

// Remove \r characters
for (let i = 0; i < result.length; i++) {
    result[i] = result[i].replace(/\r/g, '')
}

console.log(result)

// Save to a text file
fs.writeFileSync('result.txt', result.join('\n'), 'utf8');