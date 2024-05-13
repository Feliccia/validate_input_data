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
        
    # 将第一个英文字母转换为对应的数字
    first_letter = id_number[0].upper()
    if first_letter.isalpha():
        first_digit = ord(first_letter) - ord('A') + 10
    else:
        return "第一個字元應為英文字母", 400

    # 将转换后的两位数字分别乘以1和9
    first_digit *= 1
    second_digit = first_digit * 9

    # 将第二个到第九个数字分别乘以8, 7, 6, 5, 4, 3, 2, 1
    multipliers = [8, 7, 6, 5, 4, 3, 2, 1]
    other_digits = [int(digit) for digit in id_number[1:9]]
    result = sum(digit * multiplier for digit, multiplier in zip(other_digits, multipliers))

   # 将以上所有乘积相加，并加上最後一個數字
    total_sum = first_digit + second_digit + result + int(id_number[-1])

  # 如果最後的結果可以被10整除，則這個身份證號碼就是正確的
    if total_sum % 10 == 0:
        return "身分證號碼是有效的", 200
    else:
        return "身分證號碼是無效的", 400



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

