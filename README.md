**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

[[answer-img/pods.png]]  
[[/answer-img/services.png]]  

## Setup the Jaeger and Prometheus source
*TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.

[[/answer-img/grafana.png]]  

## Create a Basic Dashboard
*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.

[[/answer-img/basic-dashboard.png]]  

## Describe SLO/SLI
*TODO:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.

SLO (Service Level Objective) define certain metrics to be met over a certain period of time, such as the availability > 99% of the system in a month or the average response time < 500ms in a week.  
The SLI (Service Level Indicator) is the measurement of the defined metrics, such as the uptime of the system of 99.97% within the month or the average response time in the week of 339ms. 

## Creating SLI metrics.
*TODO:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 

general SLI:  
Abailabilty - uptime of a system, where the system is running and reachable (in %)  
response time - answer time of the system (in ms)  
error rate - amount of http 500 answers of the system (in % or total)  
specific SLI:  
Amount of 5-star ratings (per day)  
Amount of completed orders (per hour)  

## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.  

Screenshot only shows the uptime of the nodes. In normal i would prepare a dashboard with this querys for measure the http errors, but in fact that the loadbalancer setup with nginx is not workling in the lokal setup and instead i use nodeport for the k3d cluster:  

HTTP 4xx Error:  

```
sum(rate(nginx_ingress_controller_requests{controller_pod=~"$controller",controller_class=~"$controller_class",namespace=~"$namespace",status~"[4].*"}[2m])) 
```
or only filtering of the default namespace where the applications are running  

HTTP 5xx Error:  
```
sum(rate(nginx_ingress_controller_requests{controller_pod=~"$controller",controller_class=~"$controller_class",namespace=~"$namespace",status~"[5].*"}[2m])) 
```

[[/answer-img/sli-dashboard.png]]

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here. Also provide a (screenshot) sample Python file containing a trace and span code used to perform Jaeger traces on the backend service.

Code of the backend app is also uploaded to this repository. Also the edited deployment (add annotation) is included.

[[/answer-img/flask-app.png]]  
[[/answer-img/jaeger-ui.png]]  

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.

[[/answer-img/jaeger-grafana.png]]  

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue also include a screenshot of the tracer span to demonstrate how we can user a tracer to locate errors easily.

TROUBLE TICKET (trouble Ticket if we assume to have a high latency, which is not the case right now)  

Name: Thomas Müller  

Date: 20.02.2021 - 15:35    

Subject: High Latency  

Affected Area: Accessebility of the backend  

Severity: medium  

Description: The traces show, that the /api endpoint has an higher latency then usual. Normally we have a max 20 ms. At the moment the traces for /api show up to 2 seconds. If we sum up the answer time and the amount of requests we assume, that the frontend is not that responsible to the customer as usual  

Wo tecnically could implement some other logging which create 400 or 500 errors or catch all other errors, but i assume that we should write an invented trouble ticket.  

## Creating SLIs and SLOs
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.

* HTTP Status Codes with 2xx > 99,95%  
* CPU and Memory Consumption < 80%  
* Node Uptime > 99,95%  
* Responsetime < 400 ms  
* Requests per minute  

## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create a list of 2-3 KPIs to accurately measure these metrics as well as a description of why those KPIs were chosen. We will make a dashboard for this, but first write them down here.  

Uptime of the Infrastructure (general reachability of the service): Node Uptime > 99,95%  
Network Capacity: Responsetime and requests per minute - to see if the requests are handled correctly and to assume, that the application is working normal for the customer  
Infrastructure Capacity: CPU and Memory Consumption - to be sure that the infrastructue will not be the bottleneck while serving the applikation.  
Availibilty of the service / app: HTTP Status code - to make sure the applikation is working as accepted the status codes beeing monitored  

## Final Dashboard
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  

Same Problem like above to measue the Statuscodes without nginx loadbalancer i would create panels with these quereys:  

Controller Success Rate (non-4|5xx responses)  
```
sum(rate(nginx_ingress_controller_requests{controller_pod=~"$controller",controller_class=~"$controller_class",namespace=~"$namespace",status!~"[4-5].*"}[2m])) / sum(rate(nginx_ingress_controller_requests{controller_pod=~"$controller",controller_class=~"$controller_class",namespace=~"$namespace"}[2m]))
```
Requests per minute:  
```
round(sum(irate(nginx_ingress_controller_requests{controller_pod=~"$controller",controller_class=~"$controller_class",controller_namespace=~"$namespace",ingress=~"$ingress"}[1m])) by (ingress), 0.001)
```

[[/answers/kpi-dashboard.png]]