import unittest
from flask import Flask
from flask_testing import TestCase
import logging

# Import the Flask app
from Flask_app import app


class CalculatorTestCase(TestCase):

    def create_app(self):
        # Set the app's testing config variables
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

    def setUp(self):
        super().setUp()
        # Set up the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def tearDown(self):
        # Remove the logger
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def test_calculator_successful(self):
        with self.client:
            # Test a successful calculation
            response = self.client.post('/', data={
                'principal': '1000',
                'rate': '5',
                'time': '3'
            })
            self.logger.debug('Testing a successful calculation...')
            self.assert200(response)
            self.assert_template_used('calculator.html')
            self.assert_context('result', {
                'amount': 1157.63,
                'interest': 157.63
            })
            self.logger.debug('Successful calculation test passed.')

    def test_calculator_zero_principal(self):
        with self.client:
            # Test a calculation with zero principal
            response = self.client.post('/', data={
                'principal': '0',
                'rate': '5',
                'time': '3'
            })
            self.logger.debug('Testing a calculation with zero principal...')
            self.assert200(response)
            self.assert_template_used('calculator.html')
            self.assert_context('result', {
                'amount': 0.0,
                'interest': 0.0
            })
            self.logger.debug('Calculation with zero principal test passed.')

    def test_calculator_zero_rate(self):
        with self.client:
            # Test a calculation with zero rate
            response = self.client.post('/', data={
                'principal': '1000',
                'rate': '0',
                'time': '3'
            })
            self.logger.debug('Testing a calculation with zero rate...')
            self.assert200(response)
            self.assert_template_used('calculator.html')
            self.assert_context('result', {
                'amount': 1000.0,
                'interest': 0.0
            })
            self.logger.debug('Calculation with zero rate test passed.')

    def test_calculator_negative_time(self):
        with self.client:
            # Test a calculation with negative time
            response = self.client.post('/', data={
                'principal': '1000',
                'rate': '5',
                'time': '-3'
            })
            self.logger.debug('Testing a calculation with negative time...')
            self.assert200(response)
            self.assert_template_used('calculator.html')
            self.assert_context('result', {
                'amount': None,
                'interest': None
            })
            self.logger.debug('Calculation with negative time test passed.')

    def test_calculator_get_request(self):
        with self.client:
            # Test a GET request to the calculator route
            response = self.client.get('/')
            self.logger.debug('Testing a GET request to the calculator route...')
            self.assert200(response)
            self.assert_template_used('calculator.html')
            self.assert_context('result', None)
            self.logger.debug('GET request to the calculator route test passed.')


if __name__ == '__main__':
    unittest.main()
