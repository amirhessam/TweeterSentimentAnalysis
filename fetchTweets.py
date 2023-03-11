import snscrape.modules.twitter as sntwitter
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util.ssl_ import create_urllib3_context

# see "openssl ciphers" command for cipher names
CIPHERS = "ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384"

class TlsAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


class FetchTweets:
    get_tw_query = "(from:{}) until:{} since:{} -filter:replies"
    get_rep_query = "(to:{}) conversation_id:{} (filter:safe OR -filter:safe) "
    get_rep_query_min_fav = "(to:{}) conversation_id:{} (filter:safe OR -filter:safe) min_faves:{}"

    def get_tweets_for(self, account_name, start_date, end_date, reply_limit = 100, min_fav = 10):
        q = self.get_tw_query.format(account_name, end_date, start_date)
        tweet_l = []
        adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        tss = sntwitter.TwitterSearchScraper(q)
        tss._session.mount("https://", adapter)
        for t in tss.get_items():
            tweet_d = {
                'content': t.rawContent,
                'username': t.user.username,
                'date': t.date,
                'retweetCount': t.retweetCount,
                'replyCount': t.replyCount,
                'likeCount': t.likeCount,
                'viewCount': t.viewCount,
                'conversationId': t.conversationId,
                'id': t.id,
                'reply': False
            }
            rep_l = [tweet_d]
            rep_q = self.get_rep_query_min_fav.format(account_name, t.conversationId, min_fav)
            tss2 = sntwitter.TwitterSearchScraper(rep_q)
            tss2._session.mount("https://", adapter)
            for rep in (tss2.get_items()):
                rep_d = {
                    'content': rep.rawContent,
                    'username': rep.user.username,
                    'date': rep.date,
                    'retweetCount':rep.retweetCount,
                    'replyCount':rep.replyCount,
                    'likeCount':rep.likeCount,
                    'viewCount':rep.viewCount,
                    'conversationId':t.conversationId,
                    'id':rep.id,
                    'reply':True
                }
                rep_l.append(rep_d)
                if len(rep_l) > reply_limit:
                    break
            tweet_l += rep_l
        return tweet_l
