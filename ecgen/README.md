# networksConfig

# ecgen

This folder implements the Sender, Receiver and Router classes for use in the network emulation. It uses the [zfec](https://github.com/tahoe-lafs/zfec) library in python to encode packets, generate error correcting codes,
and then finally decode it at the receiver.

## Setup

Due to the large number of requirements to run ecgen, it is suggested that a conda environment is used.

```jsx
conda env create -f environment.yml
```

To run the unit tests:

```jsx
python3 tests.py
```

The `example.py` file also shows an example of how the sender and receiver nodes can be used. It can be compiled and run by doing the following command.

```jsx
python3 example.py
```

### Padding

The padding scheme used here is a trivial one which uses a DELIMITER of "`" to pad. This DELIMITER is then stripped at the receiver using python's .strip() method. More robust padding schemes such as PKCS should be employed if this is to be used to send packets containing the DELIMITER as part of the data. As part of this simple implementation, we assume that all packet data do not contain DELIMITER inside of it.

### Further notes

The packets as seen in `utils.py` are also highly simplified, where the iphdr only contains the source and destination ips, and omits all other fields of the IPv4 headers for simplicity.
