import os
import multiprocessing

wsgi_app = "app:app"

workers = int(os.environ.get("GUNICORN_PROCESSES", multiprocessing.cpu_count()))
threads = int(os.environ.get("GUNICORN_THREADS", "4"))
timeout = int(os.environ.get("GUNICORN_TIMEOUT", "30"))
bind = os.environ.get("GUNICORN_BIND", "0.0.0.0:8080")
reload = bool(os.environ.get("GUNICORN_RELOAD", "false"))

loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")

forwarded_allow_ips = "*"
secure_scheme_headers = {"X-Forwarded-Proto": "https"}
