from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate'])
        time = int(request.form['time'])

        if time < 0:
            amount = None
            interest = None
        else:
            amount = round(principal * (1 + rate / 100) ** time, 2)
            interest = round(amount - principal, 2)

        result = {
            'principal': principal,
            'rate': rate,
            'time': time,
            'amount': amount,
            'interest': interest
        }

    return render_template('calculator.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
