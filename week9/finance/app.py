import os

from cs50 import SQL
from string import ascii_lowercase, ascii_uppercase, digits
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


SPECIAL = {"!", '"', "#", "$", "%", "&", "(", ")", "*", "+", "-", ",", ".",
           "/", ":", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{",
           "}", "|", "~", }

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

    # Get user information
    user_info = db.execute(
        "SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    user_id = user_info.get("id")
    username = user_info.get("username")
    cash_balance = user_info.get("cash")

    # Get users's stock summary
    stock_summary = db.execute(
        "SELECT symbol, COUNT (CASE action WHEN 'buy' then 1 else null END) - COUNT (CASE action WHEN 'sell' then 1 else null END) as shares FROM history WHERE user_id=? GROUP BY symbol HAVING shares > 0",
        user_id,
    )

    # Initialize variable that will report total stock value + cash balance
    grand_total = user_info.get("cash")
    # Insert stock name and current stock price to stock summary
    for stock in stock_summary:
        stock_info = lookup(stock.get("symbol"))
        stock["name"] = stock_info.get("name")
        stock["price"] = stock_info.get("price")
        stock["total_value"] = stock.get("price") * stock.get("shares")
        grand_total += stock.get("price") * stock.get("shares")

    return render_template(
        "index.html",
        username=username,
        cash_balance=cash_balance,
        grand_total=grand_total,
        stock_summary=stock_summary,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("number of shares must be an integer!")
        # Ensure stock symbol was submitted
        if not symbol or (not shares and shares != 0):
            return apology("must provide symbol and shares", 400)
        elif shares <= 0:
            return apology("number of shares must be greater than zero", 400)

        stock = lookup(symbol)
        # Ensure stock symbol exists
        if not stock:
            return apology("stock doesn't exist!", 400)

        cash = db.execute(
            "SELECT cash FROM users WHERE id is (?)", session.get("user_id")
        )[0]["cash"]
        price = stock.get("price")

        # Ensure user has funds to buy stock at requested volume
        if price * shares >= cash:
            return apology("user does not have funds to buy stocks")

        _datetime = datetime.now()
        date = int(_datetime.strftime("%d%m%Y"))
        time = int(_datetime.strftime("%H%M%S"))
        for i in range(shares):
            db.execute(
                "INSERT INTO history"
                "(symbol, price, action, date, time, user_id)"
                "VALUES (?, ?, ?, ?, ?, ?)",
                symbol,
                price,
                "buy",
                date,
                time,
                session["user_id"],
            )

        # Remove cash from user
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            (cash - price * shares),
            session["user_id"],
        )

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/funds", methods=["GET", "POST"])
@login_required
def funds():
    """Add to or subtract from cash balance"""
    if request.method == "POST":
        try:
            adjustment = int(request.form.get("adjustment"))
        except ValueError:
            return apology("adjustment of funds must be an integer!")

        id = session["user_id"]
        db.execute("UPDATE users SET cash=cash + ? WHERE id=?",
                   adjustment, id)
        return redirect("/")
    else:
        return render_template("funds.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    history = db.execute("SELECT * FROM history WHERE user_id=?", user_id)
    return render_template("history.html", history=history)


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
            "SELECT * FROM users WHERE username = ?", request.form.get(
                "username")
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
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Ensure user provided symbol
        if not symbol:
            return apology("must provide symbol", 400)
        quote = lookup(symbol)

        # Ensure stock symbol exists
        if quote:
            return render_template("quoted.html", quote=quote)
        else:
            return apology("stock doesn't exist!", 400)
    else:
        return render_template("quote.html")


@app.route("/quoted", methods=["GET"])
@login_required
def quoted():
    if request.args.get("name"):
        return render_template("quoted.html")
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure username is not a duplicate
        user_table = db.execute("SELECT username FROM users")
        usernames = [user_dict.get('username') for user_dict in user_table]
        if username in usernames:
            return apology("username already exists!")

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 400)

        # Ensure password is complex enough
        if len(password) < 6:
            return apology("password must be 6 characters or longer", 400)
        has_digit = 0
        has_lower = 0
        has_upper = 0
        has_special = 0

        def add(has_check: int):
            has_check += 1
            return has_check
        for char in password:
            has_digit = add(has_digit) if char in digits else has_digit
            has_lower = add(has_lower) if char in ascii_lowercase else has_lower
            has_upper = add(has_upper) if char in ascii_uppercase else has_upper
            has_special = add(has_special) if char in SPECIAL else has_special

        if not has_digit:
            return apology("password must contain at least one digit", 400)
        if not has_lower:
            return apology("password must contain at least one lowercase character", 400)
        if not has_upper:
            return apology("password must contain at least one uppercase character", 400)
        if not has_special:
            return apology("password must contain at least one special character", 400)
        # Ensure confirmation mapches password
        if password != request.form.get("confirmation"):
            return apology("confirmation does not match password", 400)

        hash = generate_password_hash(password)
        # Register user
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
    else:
        return render_template("register.html")

    return render_template("login.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session["user_id"]
    stock_summary = db.execute(
        "SELECT symbol, COUNT (CASE action WHEN 'buy' then 1 else null END) - COUNT (CASE action WHEN 'sell' then 1 else null END) as shares FROM history WHERE user_id=? GROUP BY symbol HAVING shares > 0",
        user_id)

    symbols_list = [symbols_dict.get('symbol') for symbols_dict in stock_summary]
    print(symbols_list)

    if request.method == "POST":

        symbol = request.form.get("symbol")
        try:
            shares_to_sell = int(request.form.get("shares"))
        except ValueError:
            return apology("number of shares must be an integer!")
        # Ensure stock symbol was submitted
        if not symbol or (not shares_to_sell and shares_to_sell != 0):
            return apology("must provide symbol and shares", 400)
        elif shares_to_sell <= 0:
            return apology("number of shares must be greater than zero", 400)

        stock = lookup(symbol)
        # Ensure stock symbol exists
        if not stock:
            return apology("stock doesn't exist!", 400)

        # Ensure users owns that stock
        if stock.get("symbol") not in symbols_list:
            return apology("user does not own that stock", 400)

        owned_shares = stock_summary[0].get("shares")
        # Ensure user has enough shares to sell
        if shares_to_sell > owned_shares:
            return apology("not enough shares to sell", 400)

        # Get info ready for transaction update
        cash = db.execute(
            "SELECT cash FROM users WHERE id is (?)", session.get("user_id")
        )[0]["cash"]
        price = stock.get("price")
        _datetime = datetime.now()
        date = int(_datetime.strftime("%d%m%Y"))
        time = int(_datetime.strftime("%H%M%S"))

        # Add sale to transaction history
        for i in range(shares_to_sell):
            db.execute(
                "INSERT INTO history"
                "(symbol, price, action, date, time, user_id)"
                "VALUES (?, ?, ?, ?, ?, ?)",
                symbol,
                price,
                "sell",
                date,
                time,
                session["user_id"],
            )

        # Add cash to user's balance
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            (cash + price * shares_to_sell),
            session["user_id"],
        )

        return redirect("/")

    else:
        return render_template("sell.html", symbols_list=symbols_list)
    return apology("TODO")
