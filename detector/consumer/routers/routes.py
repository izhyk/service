from consumer import APP
from consumer.config import Configs


@APP.route('/get_last_offset', methods=['GET'])
async def get_last_offset(request):
    pass
