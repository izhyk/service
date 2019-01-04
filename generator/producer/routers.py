from sanic.response import html, redirect
from producer.helpers import send_one
from producer import APP, LOOP
import asyncio


@APP.route("/", methods=['GET'])
async def index(request):
    return html('''
        <form action='/send_message' method='post'>
            Your Message: <input type='text' name='message'><br>
            <input type='submit' value ='Send'>
        </form>
    ''')


@APP.route("/send_message", methods=['POST'])
async def send_message(request):
    message = request.form.get('message')

    if not message:
        message = 'Default message'

    # TODO: impossible to use LOOP from producer
    loop = asyncio.get_event_loop()
    await send_one(loop, message)
    return redirect('/')



