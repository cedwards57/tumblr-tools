class TumblrError(Exception):
    def __init__(self, response):
        try:
            self.response = response.json()
        except Exception as e:
            text = f'Tumblr returned error code {response.status_code}. Additionally, see error:\n{type(e)}: {e}'
            raise Exception(text)
        self.status = response.status_code
        if 'errors' in self.response.keys():
            self.title = self.response['errors'][0]['title']
            self.code = self.response['errors'][0]['code']
            self.msg = self.response['errors'][0]['detail']
        else:
            self.title = self.response['error']
            self.msg = self.response['error_description']
            self.code = 0
        self.error = f'{self.status}.{self.code}. {self.title}: {self.msg}'

        if self.status == 400:
            raise TumblrBadRequestError(self.error)
        if self.status == 401:
            raise TumblrUnauthorizedError(self.error)
        if self.status == 403:
            raise TumblrForbiddenError(self.error)
        if self.status == 404:
            raise TumblrNotFoundError(self.error)
        if self.status == 429:
            raise TumblrRateLimitError(self.error)
        if self.status == 500:
            raise TumblrServerError(self.error)
        if self.status == 503:
            raise TumblrServiceError(self.error)
        else:
            super().__init__(self.error)
        

class TumblrBadRequestError(Exception):
    pass

class TumblrUnauthorizedError(Exception):
    pass

class TumblrForbiddenError(Exception):
    pass

class TumblrNotFoundError(Exception):
    pass

class TumblrRateLimitError(Exception):
    pass

class TumblrServerError(Exception):
    pass

class TumblrServiceError(Exception):
    pass