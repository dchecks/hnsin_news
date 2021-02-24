from urllib.parse import urlparse


class Article():
    def __init__(self,
                 hn_id,
                 title,
                 article_url,
                 score,
                 number_of_comments,
                 submitter,
                 timestamp,
                 ):
        self.hn_id = hn_id
        self.title = title
        self.article_url = article_url
        self.score = score
        self.number_of_comments = number_of_comments
        self.submitter = submitter
        self.timestamp = timestamp

    @property
    def get_absolute_url(self):
        return self.article_url or "https://news.ycombinator.com/item?id=" + str(self.hn_id)

    @property
    def site(self):
        if not self.article_url:
            return None
        else:
            netloc = urlparse(self.article_url).netloc
            path = netloc.split(".")
            try:
                return path[-2] + "." + path[-1]
            except:
                return netloc