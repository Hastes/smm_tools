import facebook


class FacebookUser():

    def __init__(self, token):
        self.graph = facebook.GraphAPI(access_token=token)
        self.api_version = 'v3.3'

    def call(self, func_name, method="POST", data=None, params=None):
        path = '{0}/{1}/{2}'.format(self.api_version, 'me', func_name)
        response = self.graph.request(
            path=path,
            method=method,
            post_args=data,
            args=params
        )
        return response

    def get_account_id(self):
        resp = self.call('adaccounts', 'GET')
        self.get_pages()
        return resp['data'][0]['id']

    def get_pages(self):
        resp = self.call('accounts', 'GET')
        return resp['data']
