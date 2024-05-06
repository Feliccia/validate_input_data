from flask import Flask, request, render_template
import re

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('input_data.html')

@app.route('/submit_form', methods=['POST'])
def handle_form():
    id_number = request.form.get('id')
    name = request.form.get('name')
    gender = request.form.get('gender')
    email = request.form.get('email')

    # Validate ID number (assuming 台灣ID)
    if len(id_number)!=10:
        return "身分證號碼應該為10碼", 400
    if not id_number[0].isalpha():
        return "第一個字元應為英文字母", 400
    if not id_number[1:].isdigit():
        return "後九個字元應該為數字", 400
        
    # Convert first character to corresponding number
    first_char_value = ord(first_char.upper()) - ord('A') + 10

    if first_char_value < 10 or first_char_value > 33:
        return "第一個字元應為英文字母(A-Z)", 400

    # Multiply converted number by 1 and 9
    first_digit = first_char_value // 10
    second_digit = first_char_value % 10

    first_result = first_digit * 1
    second_result = second_digit * 9

    # Multiply the second to ninth digits by 8, 7, 6, 5, 4, 3, 2, 1 respectively
    multipliers = [8, 7, 6, 5, 4, 3, 2, 1]
    other_digits = id_number[1:]
    other_results = [int(digit) * multiplier for digit, multiplier in zip(other_digits, multipliers)]

    # Sum up all the products
    total = first_result + second_result + sum(other_results)

    # Add the last digit of the ID number
    last_digit = int(id_number[-1])
    total += last_digit

    # Check if the total is divisible by 10
    if total % 10 == 0:
        return "身分證號碼正確"
    else:
        return "身分證號碼錯誤"


    # Validate name (assuming it's alphabetic)
    if not re.match(r'^[A-Za-z\s]+$', name):
        return "Invalid name", 400

    # Validate gender
    if gender not in ['Male', 'Female']:
        return "Invalid gender", 400

    # Validate email
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return "Invalid email", 400

    return "All entries are valid", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Listen on all available network interfaces and port 80

