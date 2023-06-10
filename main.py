from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from tradingstrategy import trading_strategy_1


app = Flask(__name__)
api = Api(app)


class Hello(Resource):

    def get(self):
        return jsonify({'message': 'Hello World'})

    def post(self):
        data = request.get_json()
        return jsonify({'data': data})


class TradingStrategy(Resource):

    def get(self):
        return jsonify({'stocks': trading_strategy_1()})


api.add_resource(Hello, '/')
api.add_resource(TradingStrategy, '/tradingstrategy')


if __name__ == '__main__':
    app.run(debug=True)