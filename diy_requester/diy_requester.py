import json
import logging
import os

class DiyRequester:
    base_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    def __init__(self,session, central_url):
        self.session = session
        self.central_url = central_url
        self.headers = self.base_headers.copy()
        self.session.headers.update(self.headers)
        self.logger = logging.getLogger(__name__)

    def send_request(self, method, endpoint=None,expected_status=None, params=None, need_logging = True, **kwargs):
        if endpoint:
            full_url = f'{self.central_url}{endpoint}'
        else:
            full_url = self.central_url
        response = self.session.request(method,full_url,params,**kwargs)

        print(f"[{method}] {full_url} | Статус: {response.status_code}")
        # print(response.text)

        if need_logging:
            self.log_request_and_response(response)

        if expected_status:
            assert response.status_code == expected_status, f'Ошибка! Ожидали {expected_status} код, а получили {response.status_code} код'
        return response

    def log_request_and_response(self, response):
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'

            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body and body != '{}' else ''

            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            response_data = response.text

            try:
                response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                pass

            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not is_success:
                self.logger.info(
                    f"\tSTATUS_CODE: {RED}{response_status}{RESET}\n"
                    f"\tDATA: {RED}{response_data}{RESET}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {GREEN}{response_status}{RESET}\n"
                    f"\tDATA:\n{response_data}"
                )
            self.logger.info(f"{'=' * 80}\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")

