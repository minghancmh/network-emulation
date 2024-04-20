import re

def processLog(filename):
    with open(filename, 'r') as f:
        log = f.read()


    runs = log.split("*")
    NUM_PAYLOADS_TOTAL = 1000
    x_drop_rates = []
    y_redundancy_factors = []
    z_prob_decoded_msgs = []
    # print(runs)
    for run in runs:
        if run == "\n":
            continue
        # Use regular expressions to extract redundancy factors and the number of successfully decoded messages
        drop_rate = float(list(set(re.findall(r"Drop Rate:(\d+\.\d+)", run)))[0])
        redundancy_factor = float(list(set(re.findall(r"Redundancy Factor:(\d+\.\d+)", run)))[0])
        num_decoded_msgs = re.search(r"Num successfully decoded msgs: (\d+)", run)

        # Check if we found the number of decoded messages, if not, set to None or some default
        num_decoded_msgs = float(num_decoded_msgs.group(1) if num_decoded_msgs else "Not found")


        # Output the extracted values
        # print("Redundancy Factor (Unique):", set(redundancy_factors))
        # print("Number of Successfully Decoded Messages:", num_decoded_msgs)

        x_drop_rates.append(drop_rate)
        y_redundancy_factors.append(redundancy_factor)
        z_prob_decoded_msgs.append(num_decoded_msgs/1000)
    return x_drop_rates, y_redundancy_factors, z_prob_decoded_msgs



