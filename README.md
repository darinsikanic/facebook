# ST2 Facebook Integration Pack

Pack which allows integration with Facebook.

## Manual Installation

```
cp -R ./facebook /opt/stackstorm/packs
st2 run packs.setup_virtualenv packs=facebook
st2 run packs.load register=all
st2 run packs.restart_component servicename=st2sensorcontainer
```

## Configuration

* ``version`` - Facebook API version.
* ``page_id`` - [Facebook Page ID](https://developers.facebook.com/docs/graph-api/reference/v2.6/page/feed).
* ``fb_app_id`` - Facebook App ID.
* ``fb_app_secret`` - [Facebook App Secret](https://developers.facebook.com/docs/facebook-login/access-tokens#apptokens).

### Obtaining API credentials

To obtain API credentials, you need to first create a Facebook application [https://developers.facebook.com/apps](https://developers.facebook.com/apps).

Then go to the app dashboard and obtain the App ID and App Secret.

## Sensors

### FacebookSearchSensor

This sensor uses the Facebook [Graph API](https://developers.facebook.com/docs/graph-api/) to return the latest posts. For every recent post in the feed, a trigger is dispatched.