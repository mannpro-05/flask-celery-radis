from celery import Celery, Task
from flask import Flask

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

print(app.name)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])


@celery.task
def find_fibonacci_async(number):
    def fib(n):
        if n == 1:
            return 0
        if n == 2:
            return 1

        return fib(n - 1) + fib(n - 2)

    result = fib(number)
    return result


@app.route("/")
def hello():

    ans: Task = find_fibonacci_async.delay(35)
    print(ans.status)
    ans.wait()
    print(ans.status, ans.result)
    return "Hello, World!"

if __name__ == '__main__':
    app.run()