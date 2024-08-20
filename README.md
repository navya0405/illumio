# Illumio Take Home Assignment

### The program should generate an output file containing the following: 
1. Count of matches for each tag, sample o/p shown below 
2. Count of matches for each port/protocol combination

### Requirement Details
1. Input file as well as the file containing tag mappings are plain text (ascii) files  
2. The flow log file size can be up to 10 MB 
3. The lookup file can have up to 10000 mappings 
4. The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample above. 
5. The matches should be case insensitive 

### Prerequisites

Ensure you have the following installed:
- Git
- Python 3

### Installation

1. **Clone the repository**

    Open a terminal and run the following git command:

    `git clone https://github.com/navya0405/illumio.git`

2. **Navigate to the repository directory**

    Change to the cloned repository's directory:

3. **Run the application**

    Execute the following command to start the application:

    `python3 main.py`

The outputs files are,
Tag Counts - tag_counts.csv 
Port/Protocol Counts - port_protocol_counts.csv.

### Approach

#### Let's consider the below log and breakdown what each field indicates:
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK 

1. 2 - version
2. 123456789012 - account id
3. eni-0a1b2c3d - interface id
4. 10.0.1.201 - srcaddr
5. 198.51.100.2 - destaddr
6. 443 - srcport
7. 49153 - dstport
8. 6 - protocol
9. 25 - packets
10. 20000 - bytes
11. 1620140761 - start time (time when first packet was recieved) in unix
12. 1620140821 - end time (time when last packet was recieved) in unix
13. ACCEPT - action (Traffic was accepted)
14. OK - logstatus (Data is logging normally to the chosen destinations.)


#### The fields which we would be using for our analytics are 7.dstport, 8.protocol.

1. To get the Count of matches for each tag,We use the above 2 fields from flow logs and use the lookup table to map both dstport and protocol as key (tuple) to get the tag and increment the tag count based on that.
The protcol in flow logs has number code only, hence I have created a mapping of these protocol numbers below to map them to protocol given in look up table.

{'6': 'tcp', '17': 'udp', '1': 'icmp'}

The above protocol numbers were referred from -  https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml


2. To get the Count of matches for each port/protocol combination , we just create and add the count of each port protocol without using lookup table.

### Assumptions: 
1. Here count of port doesn't say if its srcport or dstport. I have taken dstport as lookup table uses dstport.
2. The code only works for the given default log format, as it checks with predefined indices, if the length or location of the protocol or dstport changes (custom logs), the code won't work. The code would still work for different version logs but with the same default log format.
3. If the length of the log is different than given default log, it will add a warning in logging and continue to next line and won't process the cusotm log line.
4. Removed case sensitivity for protocol name alone, but kept the same case for tags from look up table to match the sample output.

### Edge Cases:

1. The dstport, protocol combination in flow logs may not be found in the look up table. In that case, we can use untagged as tag as mentioned in example.
2. Changed the dstport for icmp protocol logs to 0 by default as ICMP logs don't have ports.
3. If any protocol number is not known, Unknown protocol is assigned for simplicity as I have not added all protocols in the map and olny added the protocols given in the sample.

### Testing:
 
Tested the code with sample flow logs given and also added the below logs for testing edge cases.

2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 880 17 9 4500 1620140661 1620140721 ACCEPT OK 
2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 - 1 9 4500 1620140661 1620140721 ACCEPT OK
2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 98 16 9 4500 1620140661 1620140721 ACCEPT OK 
 
It gave the below results for the above logs
880,udp,1
0,icmp,1
98,unknown,1
-,unknown,1

Untagged,11
sv_P2,1
sv_P1,2
email,3
sv_P5,1

Also tested with invalid log line with length not equal to 14:
1. 2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 880 17 9 4500 1620140661 1620140721 ACCEPT OK 123
2. 2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 880 17 9 4500 1620140661 1620140721 ACCEPT 
The above testcases added this in logging and continued to process next log line.
WARNING:root:Invalid log line length found in line: 2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 880 17 9 4500 1620140661 1620140721 ACCEPT OK 123

WARNING:root:Invalid log line length found in line: 2 123456789012 eni-4h5i6j7k 172.16.0.2 192.0.2.146 49154 880 17 9 4500 1620140661 1620140721 ACCEPT 

The outputs files are,
Tag Counts - tag_counts.csv 
Port/Protocol Counts - port_protocol_counts.csv.


### Background
1. A flow log record represents a network flow in your VPC.
2. Each record is a string with fields separated by spaces. A record includes values for the different components of the IP flow, for example, the source, destination, and protocol.

The following table describes all of the available fields for a flow log record.

Note: If a field is not applicable or could not be computed for a specific record, the record displays a '-' symbol for that entry.

<table>
  <tr>
    <th>Field</th>
    <th>Description</th>
    <th>Version</th>
  </tr>
  <tr>
    <td>version</td>
    <td>The VPC Flow Logs version. If you use the default format, the version is 2. If you use a custom format, the version is the highest version among the specified fields. For example, if you specify only fields from version 2, the version is 2. If you specify a mixture of fields from versions 2, 3, and 4, the version is 4. Parquet data type: INT_32</td>
    <td>2</td>
  </tr>
  <tr>
    <td>account-id</td>
    <td>The AWS account ID of the owner of the source network interface for which traffic is recorded. If the network interface is created by an AWS service, for example when creating a VPC endpoint or Network Load Balancer, the record might display unknown for this field. Parquet data type: STRING</td>
    <td>2</td>
  </tr>
  <tr>
    <td>interface-id</td>
    <td>The ID of the network interface for which the traffic is recorded. Parquet data type: STRING</td>
    <td>2</td>
  </tr>
  <tr>
    <td>srcaddr</td>
    <td>The source address for incoming traffic, or the IPv4 or IPv6 address of the network interface for outgoing traffic on the network interface. The IPv4 address of the network interface is always its private IPv4 address. See also pkt-srcaddr. Parquet data type: STRING</td>
    <td>2</td>
  </tr>
  <tr>
  <td>dstaddr</td>
  <td>The destination address for outgoing traffic, or the IPv4 or IPv6 address of the network interface for incoming traffic on the network interface. The IPv4 address of the network interface is always its private IPv4 address. See also pkt-dstaddr. Parquet data type: STRING</td>
  <td>2</td>
</tr>
<tr>
  <td>srcport</td>
  <td>The source port of the traffic. Parquet data type: INT_32</td>
  <td>2</td>
</tr>
<tr>
  <td>dstport</td>
  <td>The destination port of the traffic. Parquet data type: INT_32</td>
  <td>2</td>
</tr>
<tr>
  <td>protocol</td>
  <td>The IANA protocol number of the traffic. For more information, see Assigned Internet Protocol Numbers. Parquet data type: INT_32</td>
  <td>2</td>
</tr>
<tr>
  <td>packets</td>
  <td>The number of packets transferred during the flow. Parquet data type: INT_64</td>
  <td>2</td>
</tr>
<tr>
  <td>bytes</td>
  <td>The number of bytes transferred during the flow. Parquet data type: INT_64</td>
  <td>2</td>
</tr>
<tr>
  <td>start</td>
  <td>The time, in Unix seconds, when the first packet of the flow was received within the aggregation interval. This might be up to 60 seconds after the packet was transmitted or received on the network interface. Parquet data type: INT_64</td>
  <td>2</td>
</tr>
<tr>
  <td>end</td>
  <td>The time, in Unix seconds, when the last packet of the flow was received within the aggregation interval. This might be up to 60 seconds after the packet was transmitted or received on the network interface. Parquet data type: INT_64</td>
  <td>2</td>
</tr>
<tr>
  <td>action</td>
  <td>The action that is associated with the traffic: ACCEPT — The traffic was accepted. REJECT — The traffic was rejected. For example, the traffic was not allowed by the security groups or network ACLs, or packets arrived after the connection was closed. Parquet data type: STRING</td>
  <td>2</td>
</tr>
<tr>
  <td>log-status</td>
  <td>The logging status of the flow log: OK — Data is logging normally to the chosen destinations. NODATA — There was no network traffic to or from the network interface during the aggregation interval. SKIPDATA — Some flow log records were skipped during the aggregation interval. This might be because of an internal capacity constraint, or an internal error. Parquet data type: STRING</td>
  <td>2</td>
</tr>



