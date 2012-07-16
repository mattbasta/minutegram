import base64
import hmac
import time
import urllib

import constants


def mturk_url(params):

    service = services[service]

    #Step 0: add accessKey, Service, Timestamp, and Version to params
    params['AWSAccessKeyId'] = constants.AWS_KEY
    params['Service'] = "AWSMechanicalTurkRequester"

    #Amazon adds hundredths of a second to the timestamp (always .000), so we do too.
    #(see http://associates-amazon.s3.amazonaws.com/signed-requests/helper/index.html)
    params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    params['Version'] = "2006-10-31"

    #Step 1a: sort params
    paramsList = params.items()
    paramsList.sort()

    #Step 1b-d: create canonicalizedQueryString
    canonicalizedQueryString = '&'.join('%s=%s' % (k, urllib.quote(str(v))) for
                                        k, v in paramsList if v)

    #Step 2: create string to sign
    host = "mechanicalturk.amazonaws.com"
    requestUri = '/onca/xml'
    stringToSign  = 'GET\n'
    stringToSign += host +'\n'
    stringToSign += requestUri+'\n'
    stringToSign += canonicalizedQueryString.encode('utf-8')

    #Step 3: create HMAC
    digest = hmac.new(constants.AWS_SECRET, stringToSign, hashlib.sha256).digest()

    #Step 4: base64 the hmac
    sig = base64.b64encode(digest)

    #Step 5: append signature to query
    url = 'https://' + host + requestUri + '?'
    url += canonicalizedQueryString + "&Signature=" + urllib.quote(sig)

    return url
