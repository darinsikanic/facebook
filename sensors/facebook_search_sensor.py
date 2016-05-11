from st2reactor.sensor.base import PollingSensor
import dateutil.parser as dateparser
import facebook

__all__ = [
    'FacebookSearchSensor'
]

class FacebookSearchSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=None):
        super(FacebookSearchSensor, self).__init__(sensor_service=sensor_service,
                                                  config=config,
                                                  poll_interval=poll_interval)
        self._trigger_ref = 'facebook.matched_post'
        self._logger = self._sensor_service.get_logger(__name__)

    def setup(self):
        self._version = self._config.get('version', '2.6')
        self._page_id = self._config['page_id']
        self._last_post_timestamp = None
        self._args = {}

        app_id = self._config['fb_app_id']
        app_secret = self._config['fb_app_secret']
        
        self._access_token = facebook.GraphAPI().get_app_access_token(app_id=app_id, app_secret=app_secret, offline=True)
        self._graph = facebook.GraphAPI(access_token=self._access_token, version=self._version)

    def poll(self):

        last_post_timestamp = self._get_last_post_timestamp()

        if last_post_timestamp:
            self._args['since'] = last_post_timestamp

        try:
            feed = self._graph.get_connections(self._page_id, 'feed', **self._args)
        except facebook.GraphAPIError, e:
            self._logger.exception('Fetching feed for page with node_id: %s failed' % (self._page_id))
            raise e

        if 'data' in feed and feed['data']:
            posts = feed['data']
            self._set_last_post_timestamp(posts[0]['created_time'])

            for post in posts:
                self._dispatch_trigger_for_post(post=post)

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_last_post_timestamp(self):
        if not self._last_post_timestamp and hasattr(self._sensor_service, 'get_value'):
            self._last_post_timestamp = self._sensor_service.get_value(name='last_post_timestamp')
        return self._last_post_timestamp

    def _set_last_post_timestamp(self, last_post_created_time):
        self._last_post_timestamp = dateparser.parse(last_post_created_time).strftime("%Y-%m-%dT%H:%M:%S")
        if hasattr(self._sensor_service, 'set_value'):
            self._sensor_service.set_value(name='last_post_timestamp', value=self._last_post_timestamp)

    def _dispatch_trigger_for_post(self, post):
        trigger = self._trigger_ref

        payload = {
            'id': post['id'],
            'created_time': post['created_time'],
            'message': post['message']
        }
        self._sensor_service.dispatch(trigger=trigger, payload=payload)
