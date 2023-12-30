import os
import datetime
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    stocks = db.execute(
        "SELECT * FROM portfolio WHERE user = (?) ORDER BY symbol ASC",
        session["user_id"],
    )
    print(stocks)

    for stock in stocks:
        current_stock = lookup(stock["symbol"])
        stock["name"] = current_stock["name"]
        stock["price"] = current_stock["price"]
        holding_value = stock["price"] * stock["shares"]
        stock["total"] = holding_value

    # Calculate total portfolio value
    total_portfolio = 0
    for stock in stocks:
        total_portfolio += stock["total"]

    # Get current cash in wallet
    wallet = db.execute("SELECT cash FROM users WHERE id = (?)", session["user_id"])
    cash = wallet[0]["cash"]
    print(cash)

    # Calculate total cash + holdings
    net_worth = cash + total_portfolio

    return render_template("index.html", stocks=stocks, cash=cash, net_worth=net_worth)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # Display purchase form
    if request.method == "GET":
        return render_template("buy.html")

    # Make purchase
    elif request.method == "POST":
        # Check for improper input
        if not request.form.get("symbol"):
            return apology("input required", 400)

        purchase = request.form.get("symbol")
        trade = lookup(purchase)
        if not trade:
            return apology("symbol not found", 400)

        purchase_shares = request.form.get("shares")
        if not purchase_shares:
            return apology("number of shares required", 400)

        try:
            purchase_shares = int(purchase_shares)
        except ValueError:
            return apology("whole number of shares required", 400)

        if int(purchase_shares) < 1:
            return apology("positive number of shares required", 400)

        share_price = trade["price"]
        trade_cost = int(purchase_shares) * share_price
        cash_list = db.execute(
            "SELECT cash FROM users WHERE id = (?)", (session["user_id"])
        )

        # extract int of cash available from dict inside list:
        cash = cash_list[0]["cash"]
        print(cash)

        if cash < trade_cost:
            return apology("insufficient funds", 400)
        else:
            updated_cash = cash - trade_cost
        # Update purchase history database
        now = datetime.datetime.now()
        date = now.date()
        time = now.time()

        # Add trade to trades db (trade history)
        db.execute(
            "INSERT INTO trades (tradeuser, date, time, symbol, number, price) VALUES(?, ?, ?, ?, ?, ?)",
            session["user_id"],
            date,
            time,
            purchase,
            purchase_shares,
            share_price,
        )

        # For history add to new history db
        stocks_list = db.execute(
            "SELECT symbol FROM portfolio WHERE user = (?)", session["user_id"]
        )
        for stock in stocks_list:
            # If already own shares of this stock, update # of shares
            if stock["symbol"] == purchase:
                old_shares_list = db.execute(
                    "SELECT shares FROM portfolio WHERE user = (?) AND symbol = (?)",
                    session["user_id"],
                    purchase,
                )
                old_shares = old_shares_list[0]["shares"]
                updated_shares = old_shares + int(purchase_shares)
                db.execute(
                    "UPDATE portfolio SET (shares) = (?) WHERE user = (?) AND symbol = (?)",
                    updated_shares,
                    session["user_id"],
                    purchase,
                )
                return redirect("/")

        # Update cash available
        db.execute(
            "INSERT INTO portfolio (user, symbol, shares) VALUES(?, ?, ?)",
            session["user_id"],
            purchase,
            purchase_shares,
        )
        db.execute(
            "UPDATE users SET cash = (?) WHERE id = (?)",
            updated_cash,
            session["user_id"],
        )
        return redirect("/")


@app.route("/cash", methods=["GET", "POST"])
@login_required
def cash():
    """Add cash to user's wallet"""
    # Get current cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = (?)", session["user_id"])

    # Route if form is submitted
    if request.method == "POST":
        # Calculate new balance
        current_cash = cash[0]["cash"]
        deposit = request.form.get("amount")

        if not deposit:
            return apology("deposit amount required", 400)

        try:
            deposit = float(deposit)
        except ValueError:
            return apology("numeric input required", 400)

        if float(deposit) < 0.01:
            return apology("Positive amount required \n format: $0.00", 400)

        updated_cash = current_cash + float(deposit)

        # Update db's with new amount and history
        now = datetime.datetime.now()
        date = now.date()
        time = now.time()
        db.execute(
            "UPDATE users SET cash = (?) WHERE id = (?)",
            updated_cash,
            session["user_id"],
        )
        db.execute(
            "INSERT INTO trades(tradeuser, date, time, symbol, number, price, activity) VALUES (?, ?, ?, 'DEPOSIT', '0', (?), 'cash deposit')",
            session["user_id"],
            date,
            time,
            deposit,
        )

        # Display page with updates amount
        return render_template("deposited.html", cash=updated_cash)

    # Display deposit form
    else:
        return render_template("cash.html", current_cash=cash[0]["cash"])


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    trades = db.execute(
        "SELECT * FROM trades WHERE tradeuser = (?) ORDER BY date DESC, time DESC",
        session["user_id"],
    )

    # Calculate total trade cost from price & number of shares
    for trade in trades:
        trade["trade_price"] = trade["price"] * trade["number"]

    return render_template("history.html", trades=trades)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

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

    # Get symbol to lookup
    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock_quote = lookup(symbol)
        print(stock_quote)

        # Display html with quote
        if stock_quote != None:
            name = stock_quote["name"]
            price = stock_quote["price"]
            abbreviation = stock_quote["symbol"]
            return render_template(
                "quoted.html", name=name, price=price, abbreviation=abbreviation
            )

        else:
            return apology("invalid stock symbol", 400)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check username
        if not username:
            return apology("must provide username", 400)
        check = db.execute("SELECT username FROM users")
        for user in check:
            if username in user["username"]:
                return apology("username taken", 400)

        # check password
        if not password:
            return apology("must provide password", 400)
        if not confirmation:
            return apology("must verify password", 400)
        if password != confirmation:
            return apology("passwords must match", 400)

        # complete registration
        hashword = generate_password_hash(password)

        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, hashword
        )
        id = db.execute("SELECT id FROM users WHERE username = (?)", username)
        session["user_id"] = id[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        holdings = db.execute(
            "SELECT * FROM portfolio WHERE user = (?)", session["user_id"]
        )
        print(session["user_id"])
        print(holdings)
        return render_template("/sell.html", holdings=holdings)

    elif request.method == "POST":
        # Check for improper input - symbol
        if not request.form.get("symbol"):
            return apology("symbol required", 400)

        sale_symbol = request.form.get("symbol")
        trade = lookup(sale_symbol)
        if not trade:
            return apology("symbol not found", 400)

        # Check for improper input - number of shares
        if not request.form.get("shares"):
            return apology("shares required", 400)

        sale_shares = request.form.get("shares")
        try:
            sale_shares = int(sale_shares)
        except ValueError:
            return apology("whole number of shares required", 400)

        if sale_shares < 1:
            return apology("whole number of shares required", 400)

        owned_shares_list = db.execute(
            "SELECT shares FROM portfolio WHERE symbol = (?)", sale_symbol
        )
        if not owned_shares_list:
            return apology("you do not own any shares of this stock", 400)

        owned_shares = owned_shares_list[0]["shares"]
        if int(sale_shares) > owned_shares:
            return apology("insufficient shares owned", 400)

        # Calculate cost of sale
        share_price = trade["price"]
        trade_price = int(sale_shares) * share_price
        print(trade_price)

        # Remove shares from portfolio
        new_shares = owned_shares - int(sale_shares)
        if new_shares > 0:
            db.execute(
                "UPDATE portfolio SET shares = (?) WHERE symbol = (?)",
                new_shares,
                sale_symbol,
            )
        elif new_shares == 0:
            db.execute("DELETE FROM portfolio WHERE symbol = (?)", sale_symbol)

        # Add cash to portfolio
        cash_list = db.execute(
            "SELECT cash FROM users WHERE id = (?)", session["user_id"]
        )
        cash = cash_list[0]["cash"]
        updated_cash = cash + trade_price
        db.execute(
            "UPDATE users SET cash = (?) WHERE id = (?)",
            updated_cash,
            session["user_id"],
        )

        # Record transaction in trade history
        now = datetime.datetime.now()
        date = now.date()
        time = now.time()
        db.execute(
            "INSERT INTO trades(tradeuser, date, time, symbol, number, price, activity) VALUES (?, ?, ?, ?, ?, ?, 'sale')",
            session["user_id"],
            date,
            time,
            sale_symbol,
            sale_shares,
            share_price,
        )

        return redirect("/")
