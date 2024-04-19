import random
text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris commodo sollicitudin pharetra. Morbi nisi elit, hendrerit quis suscipit at, fringilla ac massa. Quisque tempus neque ipsum, eu pulvinar ex lobortis ac. Quisque venenatis elementum nulla vel efficitur. Vivamus sit amet sem vel leo venenatis iaculis. Proin in pulvinar nulla. Integer vulputate faucibus lacus at iaculis. Nunc eleifend, ex quis varius ullamcorper, nunc tortor aliquet purus, eu efficitur augue diam quis eros. In fermentum pellentesque ante. Etiam non finibus lorem. Sed non ipsum sapien. Praesent aliquam ex et sem gravida, vel consectetur nisi malesuada. Quisque fringilla nisl id felis faucibus malesuada. Nunc dignissim, metus vitae varius lobortis, risus leo ornare sapien, non vestibulum massa odio nec nunc. Cras id eros id libero sodales commodo eget et mi. Nunc tristique in velit ut elementum. Ut at dolor non justo luctus euismod a quis ligula. Maecenas in elementum justo, et egestas nunc. Ut lectus augue, elementum vel leo vel, bibendum fermentum felis. Proin id accumsan erat. Duis luctus arcu in metus varius, non lacinia tellus volutpat. Curabitur lorem est, vulputate vitae tincidunt a, dapibus id nibh. Interdum et malesuada fames ac ante ipsum primis in faucibus. Morbi a dictum orci. Curabitur blandit dui."

textList = text.split(" ")

filename = "sampleText"
for i in range(1000):
    with open(filename+str(i+1)+".txt", 'w') as f:
        random.shuffle(textList)
        newstr = " ".join(textList)
        f.write(newstr)