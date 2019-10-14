# coding=utf-8

"""
HitBTC.py

Author:        Benjamin Herrera
Date Created:  24 April 2018
Last Modified: 23 August 2019
"""

# Import
import requests

# Class of HitBTC
class HitBTC(object):
    """
    List of API functions by HitBTC's API

    API Functions Not Included: /order                        [POST]
                                /order/{clientOrderID}        [PATCH]
                                /account/crypto/withdraw/{id} [PUT]
    """
    def __init__(self, public_key, private_key):
        """
        Constructor of the HitBTC class

        :param public_key: String, uses the given public key to access layouts's account
        :param private_key: String, uses the given private key to access layouts's account
        """
        # Allocates given values into fields
        self.public_key    = public_key
        self.private_key   = private_key

        self.session       = requests.session()
        self.session.auth  = (public_key, private_key)

        self.url           = "https://api.hitbtc.com/api/2"

    def get_url(self):
        """
        Returns url

        :return: String, url
        """
        return self.url

    def get_public_key(self):
        """
        Returns public_key

        :return: String, public_key
        """
        return self.public_key

    def get_private_key(self):
        """
        Returns private_key

        :return: String, private_key
        """
        return self.private_key

    def set_url(self, url):
        """
        Changes url

        :param url: String, value to change base url
        """
        self.url = url

    def set_public_key(self, public_key):
        """
        Changes public_key

        :param public_key: String, public key to change
        """
        self.public_key = public_key

    def set_private_key(self, private_key):
        """
        Changes private_key

        :param private_key: String, private key to change
        """
        self.private_key = private_key

    def get_symbols(self):
        """
        Returns a list of paired currency symbols in JSON
        /public/symbol

        :return: JSON Text containing list of paired currency symbols
        """
        return self.session.get("%s/public/symbol/"
                                % self.url).json()

    def get_symbol_info(self, symbol):
        """
        Returns the details about the symbol
        /public/symbol/{symbol}

        :param symbol: String, Symbol to obtain details
        :return: JSON Text containing details about the given symbol
        """
        return self.session.get("%s/public/symbol/%s"
                                % (self.url, symbol)).json()

    def get_available_currencies(self):
        """
        Returns a list of available currencies
        /public/currency

        :return: JSON Text containing list of available currencies
        """
        return self.session.get("%s/public/currency/"
                                % self.url).json()

    def get_available_currency_info(self, currency):
        """
        Returns the details about the currency
        /public/currency/{currency}

        :param currency: String, currency to obtain details
        :return: JSON Text containing details about the given currency
        """
        return self.session.get("%s/public/currency/%s"
                                % (self.url, currency)).json()

    def get_ticker_list(self):
        """
        Returns a list of tickers
        /public/ticker

        :return: Json Text containing a list of tickers
        """
        return self.session.get("%s/public/ticker/"
                                % self.url).json()

    def get_ticker_for_symbol(self, symbol):
        """
        Returns the ticker for the specified symbol
        /public/ticker/{symbol}

        :param symbol: String, symbol to obtain ticker details
        :return: JSON Text containing the details of the ticker
        """
        return self.session.get("%s/public/ticker/%s"
                                % (self.url, symbol)).json()

    def get_trades(self, symbol, sort="DESC", by="timestamp", limit=100):
        """
        Returns the live trades being made in the specified symbol
        /public/trades/{symbol}

        :param sort: String, default value is DESC
        :param by: String, default value is timestamp
        :param limit: Integer, maximum number of current trades
        :param symbol: String, symbol to obtain current trades
        :return: Json Text containing that details
        """
        return self.session.get("%s/public/trades/%s?sort=%s&by=%s&limit=%s"
                                % (self.url, symbol, sort, by, limit)).json()

    def get_order_book(self, symbol, limit=100):
        """
        Return the order book for the specified symbol
        /public/orderbook/{symbol}

        :param limit: Integer, maximum number of current offers
        :param symbol: String, symbol to obtain orderbook
        :return: JSON Text containing that details
        """
        return self.session.get("%s/public/orderbook/%s?limit=%s"
                                % (self.url, symbol, limit)).json()

    def get_candles(self, symbol, period, limit=100):
        """
        Return the candles of the specified symbol
        /public/candles/{symbol}

        :param period: Integer, the time length an individual candle represents
        :param limit: Integer, maximum number of candles
        :param symbol: String, symbol to obtain candles
        :return: JSON Text containing that details
        """
        return self.session.get("%s/public/candles/%s?limit=%s&period=%s"
                                % (self.url, symbol, limit, period)).json()

    def get_orders(self, symbol):
        """
        Returns a list of currently open orders
        /order

        :param symbol: String, symbol to obtain open orders
        :return: JSON Text containing list of open orders
        """
        return self.session.get("%s/order?symbol=%s"
                                % (self.url, symbol)).json()

    def delete_all_open_orders(self, symbol):
        """
        Cancels all order for the specified ticker
        /order

        :param symbol: String, symbol to cancel all orders
        :return: JSON Text containing details about canceled orders
        """
        # Local Variable
        data = {'symbol': symbol}

        # Returns or cancels orders
        return self.session.delete("%s/order/"
                                   % self.url, data=data).json()

    def get_single_order(self, client_order_id):
        """
        Retrieves details about the specified order
        /order/{clientOrderID}

        :param client_order_id: String, order ID
        :return: JSON Text containing details about the order
        """
        return self.session.get("%s/order/%s"
                                % (self.url, client_order_id)).json()

    def put_order(self, client_order_id, symbol, side, type_order, quantity="10", price="0.0001"):
        """
        Creates an order to buy or sell currency
        /order/{clientOrderID}

        :param client_order_id: String, order ID
        :param symbol: String, market in which layouts wishes to enter or exit
        :param side: String, either sell or bu
        :param type_order: String, the type of buying or selling
        :param quantity: String, amount to buy
        :param price: String, specified value in which what price to enter or exit
        :return: JSON Text detailing details about the order
        """
        # Local Variable
        data = {'symbol': symbol, 'side': side, 'type': type_order, 'quantity': quantity, 'price': price}

        # Returns or places an order
        return self.session.put("%s/order/%s"
                                % (self.url, client_order_id), data=data).json()

    def delete_order(self, client_order_id):
        """
        Cancels specified order
        /order/{clientOrderID}

        :param client_order_id: String, order ID
        :return: JSON Text detailing details about the cancel
        """
        return self.session.delete("%s/order/%s" %
                                   (self.url, client_order_id)).json()

    def get_trading_balance(self):
        """
        Retrieves details about account's trading balance
        /trading/balance

        :return: JSON Text detailing account's trading balance
        """
        return self.session.get("%s/trading/balance"
                                % self.url).json()

    def get_trade_history(self, symbol, limit):
        """
        Retrieves account's history of trades
        /history/trades

        :param symbol: String, symbol to obtain history of trades
        :param limit: String, indicates the maximum number of trades that can be displayed
        :return: JSON Text detailing account's history of trades
        """
        return self.session.get("%s/history/trades?symbol=%s&sort=DESC&by=timestamp&limit=%s"
                                % (self.url, symbol, limit)).json()

    def get_order_history(self, symbol, limit):
        """
        Retrieves account's history of orders
        /history/order

        :param symbol: String, symbol to obtain history of orders
        :param limit: String, indicates the maximum number of orders that can be displayed
        :return: JSON Text detailing account's history of orders
        """
        return self.session.get("%s/history/order?symbol=%s&limit=%s"
                                % (self.url, symbol, limit)).json()

    def get_specified_order_history(self, id):
        """
        Retrieves history of the specified order
        /history/order/{id}/trades

        :param id: Integer, order ID
        :return: JSON Text detailing the specified order's history
        """
        return self.session.get("%s/history/order/%s/trades"
                                % (self.url, id)).json()

    def get_account_balance(self):
        """
        Retrieves details about account's balance
        /account/balance

        :return: JSON Text detailing account's balance
        """
        return self.session.get("%s/account/balance"
                                % self.url).json()

    def get_account_transactions(self):
        """
        Retrieves details about account's transactions
        /account/transactions

        :return: Json Text detailing account transactions
        """
        return self.session.get("%s/account/transactions"
                                % self.url).json()

    def get_account_transactions_by_id(self, id):
        """
        Retrieves details about a specific transaction
        /account/transactions/{id}

        :param id: String, id to obtain transaction details
        :return: JSON Text detailing the specific transaction
        """
        return self.session.get("%s/account/transactions/%s"
                                % (self.url, id)).json()

    def post_withdraw_crypto(self, currency, amount, address):
        """
        Sends specified amount of specified currency to specified wallet
        /account/crypto/withdraw

        :param currency: String, currency to send
        :param amount: String, amount being sent
        :param address: String, destination of sent amount
        :return: JSON Text detailing details of the withdrawal
        """
        # Local Variables
        data = {'currency': currency, 'amount': amount, 'address': address, 'autoCommit': True}

        # Return or withdraws amount
        return self.session.post("%s/account/crypto/withdraw"
                                 % self.url, data=data).json()

    def delete_rollback_withdraw_crypto(self, id):
        """
        Cancels specific withdrawal
        /account/crypto/withdraw/{id}

        :param id: String, id to cancel withdrawal
        :return: JSON Text detailing the removal of the withdrawal
        """
        return self.session.delete("%s/account/crypto/withdraw/%s"
                                   % (self.url, id)).json()

    def get_deposit_address(self, currency):
        """
        Retrieves deposit address of specified currency
        /account/crypto/address/{currency}

        :param currency: String, currency to obtain deposit address
        :return: JSON Text detailing specified currency deposit address
        """
        return self.session.get("%s/account/crypto/address/%s"
                                % (self.url, currency)).json()

    def post_create_new_deposit_address(self, currency):
        """
        Creates a new deposit address for specified currency
        /account/crypto/address/{currency}

        :param currency: String, currency to create new deposit address
        :return: JSON Text detailing the new deposit address
        """
        return self.session.post("%s/account/crypto/address/%s"
                                 % (self.url, currency)).json()

    def post_transfer_amount_to_trading(self, currency, amount, type):
        """
        Transfers amount of currency to main or trading
        /account/transfer

        :param currency: String, currency to transfer
        :param amount: String, amount to transfer
        :param type: String, transfer amount either to trading or main (bankToExchange or exchangeToBank)
        :return: JSON Text detailing the transfer
        """
        # Local Variable
        data = {'currency': currency, 'amount': amount, 'type': type}

        # Return or transfers amount
        return self.session.post("%s/account/transfer"
                                 % self.url, data=data).json()
