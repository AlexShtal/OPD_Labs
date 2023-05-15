from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate'])
        time = int(request.form['time'])

        amount = round(principal * (1 + rate / 100) ** time, 2)
        interest = round(amount - principal, )

        return render_template('result.html', amount=amount, interest=interest)

    return render_template('calculator.html')


if __name__ == '__main__':
    app.run(debug=True)
