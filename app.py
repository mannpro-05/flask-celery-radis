from celery import Celery, Task
from celery.signals import after_task_publish, task_success, task_postrun, task_failure
from flask import Flask

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

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


@after_task_publish.connect
def publish(sender=None, headers=None, body=None, **kwargs):
    print("Task Registered!", headers)


@task_postrun.connect
def post_run(**kwargs):
    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!")
    f.close()


@task_success.connect(sender=find_fibonacci_async)
def task_success_notifier(sender=None, **kwargs):
    with open('text.txt', 'w') as file:
        file.write('manasdasdsadasdasnn')
        file.close()
    print('hellll1ooasasdasdasdasdwqeqwe3w21233423141234123ddsqf ewfqdaskdas')




@app.route("/")
def hello():
    ans: Task = find_fibonacci_async.delay(35)
    return "Hello, World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
