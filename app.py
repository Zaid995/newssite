from flask import Flask, render_template, jsonify
from tester import GetNews
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


def scrape_all():
    with app.app_context():
        scrape = GetNews()
        scrape.scrape_all()


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(scrape_all, 'interval', minutes=1)
scheduler.start()


@app.route('/')
def get_data():
    return render_template('index.html')


@app.route('/index.html')
def all():
    return render_template('index.html')


@app.route('/sport.html')
def sport():
    return render_template('sport.html')


@app.route('/skopje.html')
def skopje():
    return render_template('skopje.html')


@app.route('/macedonia.html')
def macedonia():
    return render_template('macedonia.html')


@app.route('/economy.html')
def economy():
    return render_template('economy.html')


@app.route('/culture.html')
def culture():
    return render_template('culture.html')


@app.route('/business.html')
def business():
    return render_template('business.html')


@app.route('/balkan.html')
def balkan():
    return render_template('balkan.html')

@app.route('/albania.html')
def albania():
    return render_template('albania.html')

#@app.route('/America.html')
#def America():
#    return render_template('america.html')
#@app.route('/america.html')
#def america():
#    return render_template('america.html')


if __name__ == '__main__':
    app.run(debug=True)
