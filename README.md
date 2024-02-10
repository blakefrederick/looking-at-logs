## Taking a look at nginx logs

It's just another repository that's focussed on me learning things, and notsomuch on producing useful output. But this is education and education is useful. So there's that. Anyhow, there is some functionality here but again, it's not meant for actual useful use.

To use, find your nginx log and drop it in nginx-log.txt. Then run these with python.

`responses.py`

<img width="600" alt="graph showing response code distribution" src="https://github.com/blakefrederick/looking-at-logs/assets/4672139/0a7389b8-fff4-4f7b-a2ec-8abf514de07b">

`sizes.py`

<img width="600" alt="scatter plot of log response sizes by time of day" src="https://github.com/blakefrederick/looking-at-logs/assets/4672139/f208a7f3-d6cb-4b68-9347-11baef9b0374">

`visits.py`

<img width="600" alt="just a moving average of visits over time" src="https://github.com/blakefrederick/looking-at-logs/assets/4672139/95b2bc83-55b0-4ce0-ba1d-004d4f8f766e">

