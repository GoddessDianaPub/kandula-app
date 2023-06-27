import prometheus_client
from flask import Flask, render_template

app = Flask(__name__)
page_hits_counter = Counter('kandula_page_hits_total', 'Number of times each page was hit')
inprogress_requests_gauge = Gauge('kandula_inprogress_requests', 'Number of in-progress requests')

def handle_page_request(page):
    page_hits_counter.labels(page=page).inc()

    process_request(page)

def process_request(page):
    inprogress_requests_gauge.inc()

@app.route('/')
def home():
    handle_page_request('Home')
    return 'Home Page'

@app.route('/instances')
def instances():
    handle_page_request('Instances')
    return 'Instances Page'

@app.route('/scheduling')
def scheduling():
    handle_page_request('Scheduling')
    return 'Scheduling Page'

@app.route('/metrics')
def metrics():
    handle_page_request('Metrics')
    return 'Metrics Page'

@app.route('/health')
def health():
    handle_page_request('Health')
    return 'Health Page'

@app.route('/about')
def about():
    handle_page_request('About')
    return 'About Page'
    
import prometheus_client

@app.route('/dashboard')
def dashboard():
    prometheus_metrics = prometheus_client.generate_latest()
    parsed_metrics = prometheus_client.parser.text_string_to_metric_families(prometheus_metrics)

    metrics_dict = {}
    for metric in parsed_metrics:
        metric_name = metric.name
        metric_data = {}
        for sample in metric.samples:
            labels = {key: value for key, value in sample.labels.items()}
            metric_data[sample.name] = (sample.value, labels)
        metrics_dict[metric_name] = metric_data

    return render_template('dashboard.html', prometheus_metrics=metrics_dict, title='Dashboard')


if __name__ == '__main__':
    app.run()
