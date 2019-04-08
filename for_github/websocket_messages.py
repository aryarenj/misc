import re
from mitmproxy import ctx

from mitmproxy import io
#from mitmproxy.io import FlowReader



def websocket_message(flow):
    # get the latest message
    message = flow.messages[-1]

    # simply print the content of the message
    ctx.log.info(message.content)

    # manipulate the message content
    message.content = re.sub(r'^Hello', 'HAPPY', message.content)

filename = 'requests1.mitm'

with open(filename, 'rb') as fp:
    reader = io.FlowReader(fp)
    #while(1):

    for flow in reader.stream():
        websocket_message(flow)

