from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp

from population import Population
from log import Log

app = Flask(__name__)

# debugging
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response


# configure session
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/found", methods=["GET", "POST"])
def found():
    if request.method == "POST":
        return render_template("show.html")
    else:
        return render_template("found.html")


def escape(s):
    for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                     ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
        s = s.replace(old, new)
    return s


def extinct(top="", bottom=""):
    return render_template("extinct.html", top=escape(top), bottom=escape(bottom))


def overpop(top="", bottom=""):
    return render_template("overpop.html", top=escape(top), bottom=escape(bottom))


@app.route("/find", methods=["GET", "POST"])
def find():
    if request.method == "POST":
        if not request.form.get("pop_size"):
            return extinct("must provide a pop size")

        pop_size_temp = request.form.get("pop_size")
        pop_size_got = int(pop_size_temp)
        if pop_size_got <= 0:
            return extinct("you have to start off at least from 1 individual")
        elif pop_size_got > 3000:
            return overpop("too big starting population")

        else:
            def main():

                world_size = 128
                pop_size = pop_size_got
                mutation_rate = 0.01
                meta_mutation = 0.66
                meta_mutation_range = 0.0025  # from paper
                resource_freq = 1
                plotting = True
                iterations = 100
                pop_log = Population(world_size=world_size,
                                     pop_size=pop_size,
                                     mutation_rate=mutation_rate,
                                     meta_mutation=meta_mutation,
                                     meta_mutation_range=meta_mutation_range,
                                     resource_freq=resource_freq,
                                     iterations=iterations,
                                     plotting=plotting,
                                     progress=True).evolve()
                if plotting:
                    pop_log.plot_world()
                    pop_log.plot_stats()

            main()
            return render_template("found.html", pop_size=pop_size_got)

    else:
        return render_template("find.html")
