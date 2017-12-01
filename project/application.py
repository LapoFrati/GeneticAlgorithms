from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp

from population import Population
from log import Log
import pickle

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

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

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/learnmore")
def learnmore():
    return render_template("learnmore.html")

@app.route("/question")
def question():
    return render_template("question.html")

@app.route("/found", methods=["GET", "POST"])
def found():
    if request.method == "POST":
        return render_template("show_find.html")
    else:
        return render_template("found.html")

@app.route("/evolved", methods=["GET", "POST"])
def evolved():
    if request.method == "POST":
        return render_template("show_evolve.html")
    else:
        return render_template("evolved.html")

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
        mutation_rate_temp = request.form.get("mutation_rate")
        pop_size_got = int(pop_size_temp)
        mutation_rate_got = float(mutation_rate_temp)
        if pop_size_got <= 0:
            return extinct("you have to start off at least from 1 individual")
        elif pop_size_got > 3000:
            return overpop("too big starting population")

        else:
            def main():

                world_size = 128
                pop_size = pop_size_got
                mutation_rate = mutation_rate_got
                meta_mutation = 0.00
                meta_mutation_range = 0.0025  # from paper
                resource_freq = 1
                plotting_video = False #it would take too long to generate over and over
                plotting_stats = True
                iterations = 1000
                pop_log = Population(world_size=world_size,
                                     pop_size=pop_size,
                                     mutation_rate=mutation_rate,
                                     meta_mutation=meta_mutation,
                                     meta_mutation_range=meta_mutation_range,
                                     resource_freq=resource_freq,
                                     iterations=iterations,
                                     plotting=plotting_video,
                                     progress=True).evolve()
                if plotting_stats:
                    pop_log.plot_stats()
                if plotting_video:
                    pop_log.plot_world()
                pickle.dump(pop_log, open( "log.p", "wb" ) )

            main()
            return render_template("found.html", pop_size=pop_size_got, mutation_rate=mutation_rate_got)

    else:
        return render_template("find.html")

@app.route("/evolve", methods=["GET", "POST"])
def evolve():
    if request.method == "POST":
        if not request.form.get("pop_size"):
            return extinct("must provide a pop size")

        pop_size_temp = request.form.get("pop_size")
        mutation_rate_temp = request.form.get("mutation_rate")
        meta_mutation_temp = request.form.get("meta_mutation")
        pop_size_got = int(pop_size_temp)
        mutation_rate_got = float(mutation_rate_temp)
        meta_mutation_got = float(meta_mutation_temp)
        if pop_size_got <= 0:
            return extinct("you have to start off at least from 1 individual")
        elif pop_size_got > 3000:
            return overpop("too big starting population")

        else:
            def main():

                world_size = 128
                pop_size = pop_size_got
                mutation_rate = mutation_rate_got
                meta_mutation = meta_mutation_got
                meta_mutation_range = 0.0025  # from paper
                resource_freq = 1
                plotting_video = False #it would take too long to generate over and over
                plotting_stats = True
                iterations = 4000
                pop_log = Population(world_size=world_size,
                                     pop_size=pop_size,
                                     mutation_rate=mutation_rate,
                                     meta_mutation=meta_mutation,
                                     meta_mutation_range=meta_mutation_range,
                                     resource_freq=resource_freq,
                                     iterations=iterations,
                                     plotting=plotting_video,
                                     progress=True).evolve()
                if plotting_stats:
                    pop_log.plot_stats()
                if plotting_video:
                    pop_log.plot_world()

            main()
            return render_template("evolved.html", pop_size=pop_size_got, mutation_rate=mutation_rate_got, meta_mutation=meta_mutation_got)

    else:
        return render_template("evolve.html")
