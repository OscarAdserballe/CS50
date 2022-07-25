import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime, date



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT * FROM stock_purchases WHERE user_id=?;", user_id)

    # get user cash
    user_info = db.execute("SELECT cash FROM users WHERE id=?", user_id)
    # liquid assets
    cash = user_info[0]["cash"]
    # for total asset value at current price
    assets = cash
    # adding new key/value pair into stocks that website can access of current price
    for stock in stocks:
        stock_info = lookup(stock["stock_symbol"])
        stock["current_price"] = stock_info["price"]
        stock["total"] = round(stock["current_price"]*stock["amount_of_shares"], 2)
        assets += stock["total"]

    return render_template("index.html", stocks=stocks, assets=round(assets, 2), cash=round(cash, 2))
    #return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    now = datetime.now()
    today = date.today()

    # getting current_time and current_day
    # for history table
    CURRENT_TIME = now.strftime("%H:%M:%S")
    CURRENT_DATE = today.strftime("%d/%m/%Y")

    TIME_STAMP = CURRENT_DATE + " " + CURRENT_TIME
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        # convert str output from user into integer
        try:
            nb_shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Integer Please")
        if nb_shares <= 0:
            return apology("Please enter a positive integer")

        if not symbol or not nb_shares:
            return apology("Please fill out all fields properly")

        try:
            stock_info = lookup(symbol)
            stock_info["nb_shares"] = nb_shares
            # get price to store in table
            price = stock_info["price"]
            user_id = session["user_id"]
            user_info = db.execute("SELECT username, cash, id FROM users WHERE ?=id;", user_id)
            # testing with print(user_info[0]['username'], user_info[0]['cash'], user_info[0]['id'], user_id)
            # creating stocks table including all info about buyer and the amount of outstanding shares
            # and what price they bought at
            # table created using
            """CREATE TABLE stock_purchases
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT NOT NULL,
            user_id TEXT NOT NULL,
            stock_symbol TEXT NOT NULL,
            amount_of_shares INTEGER NOT NULL,
            price_bought_at NUMERIC NOT NULL);
            """
            # can user actually purchase that amount of shares?
            cash_needed = round(price*nb_shares, 2)
            stock_info["cash_needed"] = cash_needed
            user_cash = user_info[0]["cash"]
            if  cash_needed <= user_cash:
                # insert purchase into stock purchase table
                db.execute("INSERT INTO stock_purchases (username, user_id, stock_symbol, amount_of_shares, price_bought_at) VALUES (?, ?, ?, ?, ?);", user_info[0]["username"], user_id, symbol, nb_shares, price)
                # inserting into history table
                db.execute("INSERT INTO history (user_id, stock_symbol, amount_of_shares, price, type, time) VALUES (?, ?, ?, ?, ?, ?);", user_id, symbol, nb_shares, price, "BUY", TIME_STAMP)
                user_cash = user_cash - cash_needed
                # update user's new cash amount
                db.execute("UPDATE users SET cash=? WHERE id=?;", user_cash, user_id)
                purchase = True
            else:
                purchase = False
                return apology("Not enough cash")
        except TypeError:
            return apology("Invalid ticker symbol")

        return render_template("buy.html", stock_info=stock_info, purchase=purchase, user_cash=user_cash)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM history WHERE user_id=?;", user_id)

    return render_template("/history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        symbol = request.form.get("symbol")

        stock_info = lookup(symbol)
        # print(stock_info)
        # lookup returns None if no response from API -> incorrect ticker symbol
        if stock_info != None:
            return render_template("quote.html", stock_info=stock_info)
        else:
            return apology("Invalid ticker provided")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")
        # checking for username
        if not username:
            return apology("must provide username", 400)

        # checking for password
        elif not password:
            return apology("must provide password", 400)

        elif not confirm_password:
            return apology("must re-enter password", 400)

        elif password != confirm_password:
            return apology("Please ensure you've re-entered the same password")

        # user input has been validated sufficiently
        # input new user in SQL if not there already

        # checking if username is already used
        names = db.execute("SELECT username FROM users;")
        for user in names:
            if user['username'] == username:
                return apology("Sorry, that username is already taken")

        # username not used, hence inserting it into sql database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", username, generate_password_hash(password))

        #Go to homepage following registration
        return redirect("/")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    now = datetime.now()
    today = date.today()

    # getting current_time and current_day
    # for history table
    CURRENT_TIME = now.strftime("%H:%M:%S")
    CURRENT_DATE = today.strftime("%d/%m/%Y")

    TIME_STAMP = CURRENT_DATE + " " + CURRENT_TIME
    user_id = session["user_id"]
    stocks = db.execute("SELECT stock_symbol FROM stock_purchases WHERE user_id=?;", user_id)

    for stock in stocks:
        print(stock)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        # convert str output from user into integer
        try:
            nb_shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Integer Please", 400)

        if nb_shares <= 0:
            return apology("Please enter a positive integer", 400)

        if not symbol or not nb_shares:
            return apology("Please fill out all fields properly", 400)

        stock_info = lookup(symbol)
        stock_info["nb_shares"] = nb_shares
        if stock_info:
            # getting prerequisite user and stock info
            price = stock_info["price"]

            user_info = db.execute("SELECT username, cash, id FROM users WHERE ?=id;", user_id)

            # getting amount of stocks user has
            # will not work if there's multiple entries of the same stock. Assuming that's not the case for the meantime
            stock_user_info = db.execute("SELECT amount_of_shares FROM stock_purchases WHERE user_id=? AND stock_symbol=?;", user_id, symbol)
            shares_owned = stock_user_info[0]["amount_of_shares"]



            #info about earnings assuming they have enough shares
            cash_received = round(price*nb_shares, 2)
            stock_info["cash_received"] = cash_received
            user_cash = user_info[0]["cash"] + cash_received

            #checking if user has enough shares to sell
            if shares_owned == nb_shares:
                #deleting entry in case exact amount of shares
                db.execute("DELETE FROM stock_purchases WHERE user_id=? AND stock_symbol=?", user_id, symbol)
            elif shares_owned > nb_shares:
                # updating amount of shares in case excess owned
                db.execute("UPDATE stock_purchases SET amount_of_shares=?;", shares_owned-nb_shares)
            else:
                return apology("Not enough stocks", 400)

            #updating users' cash amount
            db.execute("INSERT INTO history (user_id, stock_symbol, amount_of_shares, price, type, time) VALUES (?, ?, ?, ?, ?, ?);", user_id, symbol, nb_shares, price, "SELL", TIME_STAMP)
            db.execute("UPDATE users SET cash=? WHERE id=?;", user_cash, user_id)

        else:
            # no info gotten from lookup()
            return apology("Invalid stock")

        return render_template("sell.html", stock_info=stock_info, stocks=stocks, user_cash=user_cash)
    else:
        return render_template("sell.html", stocks=stocks)

