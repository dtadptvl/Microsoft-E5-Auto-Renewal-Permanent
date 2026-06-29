from uvicorn import run
from quart import Quart, request, Response as quartResponse, send_file
from httpx import AsyncClient as httpx_client
from asyncio import sleep as async_sleep
from random import shuffle
from logging import getLogger
from config import *

class WebServer:
    instance = Quart(__name__)
    version = 2.1
    stats = {'version': version, 'totalRequests': 0, 'totalSuccess': 0, 'totalErrors': 0}

    def __init__(self):
        self.logger = getLogger('uvicorn')
        @self.instance.before_serving
        async def before_serve():
            host = f"127.0.0.1:{WEB_APP_PORT}" if WEB_APP_HOST == "0.0.0.0" else f"{WEB_APP_HOST}:{WEB_APP_PORT}"
            self.logger.info(f'Server running on {host}')

        @self.instance.before_request
        async def before_request():
            self.stats['totalRequests'] += 1

        ErrorHandler(self.instance)
        RouteHandler(self.instance)

class ErrorHandler:
    def __init__(self, instance: Quart):
        @instance.errorhandler(HTTPError)
        async def http_error(error: HTTPError):
            return error.description, error.status_code
    @classmethod
    def abort(cls, status_code: int = 500, description: str = None):
        raise HTTPError(status_code, description)

class HTTPError(Exception):
    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description

class RouteHandler:
    def __init__(self, instance: Quart):
        @instance.route('/call', methods=['POST'])
        async def create_task():
            json_data = await request.json
            if not json_data or json_data.get('password') != WEB_APP_PASSWORD:
                return "Unauthorized", 403
            
            access_token = await HTTPClient.acquire_access_token(
                json_data.get('refresh_token'), 
                json_data.get('client_id'), 
                json_data.get('client_secret')
            )
            instance.add_background_task(HTTPClient.call_endpoints, access_token)
            return 'Success', 201

class HTTPClient:
    instance = httpx_client()
    token_endpoint = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    graph_endpoints = ['https://graph.microsoft.com/v1.0/me', 'https://graph.microsoft.com/v1.0/users']

    @classmethod
    async def acquire_access_token(cls, refresh_token, client_id, client_secret):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token or REFRESH_TOKEN,
            'client_id': client_id or CLIENT_ID,
            'client_secret': client_secret or CLIENT_SECRET,
            'redirect_uri': 'http://localhost:53682/'
        }
        response = await cls.instance.post(cls.token_endpoint, data=data)
        res_data = response.json()
        
        # Ghi token mới để Workflow lấy
        if 'refresh_token' in res_data:
            with open('new_token.txt', 'w') as f:
                f.write(res_data['refresh_token'])
        
        if 'access_token' not in res_data:
            print(f"DEBUG ERROR: {res_data}")
            ErrorHandler.abort(401, "Token acquisition failed")
        return res_data['access_token']
    
    @classmethod
    async def call_endpoints(cls, access_token):
        headers = {'Authorization': access_token}
        for endpoint in cls.graph_endpoints:
            await async_sleep(TIME_DELAY)
            try: await cls.instance.get(endpoint, headers=headers)
            except: pass

web_server = WebServer().instance
if __name__ == '__main__':
    run(app="main:web_server", host=WEB_APP_HOST, port=WEB_APP_PORT, access_log=False)
