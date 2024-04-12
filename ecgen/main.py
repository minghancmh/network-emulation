from sender import Sender
from router import Router
from receiver import Receiver

inputToSend = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Nulla pretium lectus turpis, at tempor nisi faucibus sed. 
Morbi condimentum sodales justo, in placerat libero vestibulum eget. 
Praesent et enim felis. Duis non sagittis ipsum. Phasellus ac libero 
nec mi facilisis rhoncus. Aliquam erat volutpat. Proin vitae massa vel ante 
faucibus auctor. Suspendisse potenti. Suspendisse potenti. Cras tincidunt, 
turpis at accumsan lacinia, orci nunc interdum nisi, eget tincidunt nisl 
quam eget enim. Nulla auctor nisi vitae quam rhoncus, ac varius ipsum cursus. 
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; 
Curabitur lacinia, massa nec sollicitudin sollicitudin, risus ante dapibus nisl, 
ut auctor dolor purus et metus. Etiam a ante magna. Pellentesque sed tortor et elit 
mollis consequat finibus eget ligula. Mauris mattis nunc sit amet metus mattis, non 
dignissim mi blandit. Curabitur eget felis nec sapien tincidunt molestie non id arcu. 
Fusce sed nunc nec ligula placerat aliquam. Vestibulum nec nisi eget leo gravida posuere 
vel vitae orci. Vivamus cursus, arcu sed ullamcorper molestie, turpis ex hendrerit risus, 
at vehicula libero orci ut orci.
"""
sender = Sender(0, inputToSend, "1.1.1.1", "2.2.2.2", 11111, 22222)
sender.encode()
packets = list(sender.packetQueue)
print(packets)

print(len(packets))