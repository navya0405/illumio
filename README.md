# Illumio Take Home Assignment

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
<tr>
  <td>vpc-id</td>
  <td>The ID of the VPC that contains the network interface for which the traffic is recorded. Parquet data type: STRING</td>
  <td>3</td>
</tr>
<tr>
  <td>subnet-id</td>
  <td>The ID of the subnet that contains the network interface for which the traffic is recorded. Parquet data type: STRING</td>
  <td>3</td>
</tr>
<tr>
  <td>instance-id</td>
  <td>The ID of the instance that's associated with network interface for which the traffic is recorded, if the instance is owned by you. Returns a '-' symbol for a requester-managed network interface; for example, the network interface for a NAT gateway. Parquet data type: STRING</td>
  <td>3</td>
</tr>
<tr>
  <td>tcp-flags</td>
  <td>The bitmask value for the following TCP flags: FIN — 1 SYN — 2 RST — 4 SYN-ACK — 18 If no supported flags are recorded, the TCP flag value is 0. For example, since tcp-flags does not support logging ACK or PSH flags, records for traffic with these unsupported flags will result in tcp-flags value 0. If, however, an unsupported flag is accompanied by a supported flag, we will report the value of the supported flag. For example, if ACK is a part of SYN-ACK, it reports 18. And if there is a record like SYN+ECE, since SYN is a supported flag and ECE is not, the TCP flag value is 2. If for some reason the flag combination is invalid and the value cannot be calculated, the value is '-'. If no flags are sent, the TCP flag value is 0. TCP flags can be OR-ed during the aggregation interval. For short connections, the flags might be set on the same line in the flow log record, for example, 19 for SYN-ACK and FIN, and 3 for SYN and FIN. For an example, see TCP flag sequence. For general information about TCP flags (such as the meaning of flags like FIN, SYN, and ACK), see TCP segment structure on Wikipedia. Parquet data type: INT_32</td>
  <td>3</td>
</tr>
<tr>
  <td>type</td>
  <td>The type of traffic. The possible values are: IPv4 | IPv6 | EFA. For more information, see Elastic Fabric Adapter. Parquet data type: STRING</td>
  <td>3</td>
</tr>
<tr>
  <td>pkt-srcaddr</td>
  <td>The packet-level (original) source IP address of the traffic. Use this field with the srcaddr field to distinguish between the IP address of an intermediate layer through which traffic flows, and the original source IP address of the traffic. For example, when traffic flows through a network interface for a NAT gateway, or where the IP address of a pod in Amazon EKS is different from the IP address of the network interface of the instance node on which the pod is running (for communication within a VPC). Parquet data type: STRING</td>
  <td>3</td>
</tr>
<tr>
  <td>pkt-dstaddr</td>
  <td>The packet-level (original) destination IP address for the traffic. Use this field with the dstaddr field to distinguish between the IP address of an intermediate layer through which traffic flows, and the final destination IP address of the traffic. For example, when traffic flows through a network interface for a NAT gateway, or where the IP address of a pod in Amazon EKS is different from the IP address of the network interface of the instance node on which the pod is running (for communication within a VPC). Parquet data type: STRING</td>
  <td>3</td>
</tr>
<tr>
  <td>region</td>
  <td>The Region that contains the network interface for which traffic is recorded. Parquet data type: STRING</td>
  <td>4</td>
</tr>
<tr>
  <td>az-id</td>
  <td>The ID of the Availability Zone that contains the network interface for which traffic is recorded. If the traffic is from a sublocation, the record displays a '-' symbol for this field. Parquet data type: STRING</td>
  <td>4</td>
</tr>
<tr>
  <td>sublocation-type</td>
  <td>The type of sublocation that's returned in the sublocation-id field. The possible values are: wavelength | outpost | localzone. If the traffic is not from a sublocation, the record displays a '-' symbol for this field. Parquet data type: STRING</td>
  <td>4</td>
</tr>
<tr>
  <td>sublocation-id</td>
  <td>The ID of the sublocation that contains the network interface for which traffic is recorded. If the traffic is not from a sublocation, the record displays a '-' symbol for this field. Parquet data type: STRING</td>
  <td>4</td>
</tr>
<tr>
  <td>pkt-src-aws-service</td>
  <td>The name of the subset of IP address ranges for the pkt-srcaddr field, if the source IP address is for an AWS service. If the pkt-srcaddr belongs to an overlapped range, pkt-src-aws-service will only show one of the AWS service code. The possible values are: AMAZON | AMAZON_APPFLOW | AMAZON_CONNECT | API_GATEWAY | CHIME_MEETINGS | CHIME_VOICECONNECTOR | CLOUD9 | CLOUDFRONT | CODEBUILD | DYNAMODB | EBS | EC2 | EC2_INSTANCE_CONNECT | GLOBALACCELERATOR | KINESIS_VIDEO_STREAMS | ROUTE53 | ROUTE53_HEALTHCHECKS | ROUTE53_HEALTHCHECKS_PUBLISHING | ROUTE53_RESOLVER | S3 | WORKSPACES_GATEWAYS. Parquet data type: STRING</td>
  <td>5</td>
</tr>
<tr>
  <td>pkt-dst-aws-service</td>
  <td>The name of the subset of IP address ranges for the pkt-dstaddr field, if the destination IP address is for an AWS service. For a list of possible values, see the pkt-src-aws-service field. Parquet data type: STRING</td>
  <td>5</td>
</tr>
<tr>
  <td>flow-direction</td>
  <td>The direction of the flow with respect to the interface where traffic is captured. The possible values are: ingress | egress. Parquet data type: STRING</td>
  <td>5</td>
</tr>
<tr>
  <td>traffic-path</td>
  <td>The path that egress traffic takes to the destination. To determine whether the traffic is egress traffic, check the flow-direction field. The possible values are as follows. If none of the values apply, the field is set to -. 1 — Through another resource in the same VPC, including resources that create a network interface in the VPC 2 — Through an internet gateway or a gateway VPC endpoint 3 — Through a virtual private gateway 4 — Through an intra-region VPC peering connection 5 — Through an inter-region VPC peering connection 6 — Through a local gateway 7 — Through a gateway VPC endpoint (Nitro-based instances only) 8 — Through an internet gateway (Nitro-based instances only) Parquet data type: INT_32</td>
  <td>5</td>
</tr>
<tr>
  <td>ecs-cluster-arn</td>
  <td>AWS Resource Name (ARN) of the ECS cluster if the traffic is from a running ECS task. To include this field in your subscription, you need permission to call ecs:ListClusters. Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-cluster-name</td>
  <td>Name of the ECS cluster if the traffic is from a running ECS task. To include this field in your subscription, you need permission to call ecs:ListClusters. Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-container-instance-arn</td>
  <td>ARN of the ECS container instance if the traffic is from a running ECS task on an EC2 instance. If the capacity provider is AWS Fargate, this field will be '-'. To include this field in your subscription, you need permission to call ecs:ListClusters and ecs:ListContainerInstances. Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-container-instance-id</td>
  <td>ID of the ECS container instance if the traffic is from a running ECS task on an EC2 instance. If the capacity provider is AWS Fargate, this field will be '-'. To include this field in your subscription, you need permission to call ecs:ListClusters and ecs:ListContainerInstances. Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-container-id</td>
  <td>Docker runtime ID of the container if the traffic is from a running ECS task. If there are one or more containers in the ECS task, this will be the docker runtime ID of the first container. To include this field in your subscription, you need permission to call ecs:ListClusters. Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-second-container-id</td>
  <td>Docker runtime ID of the container if the traffic is from a running ECS task. If there are more than one containers in the ECS task, this will be the Docker runtime ID of the second container. To include this field in your subscription, you need permission to call ecs:ListClusters. Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-service-name</td>
  <td>Name of the ECS service if the traffic is from a running ECS task and the ECS task is started by an ECS service. If the ECS task is not started by an ECS service, this field will be '-'. To include this field in your subscription, you need permission to call ecs:ListClusters and ecs:ListServices. Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-task-definition-arn</td>
  <td>ARN of the ECS task definition if the traffic is from a running ECS task. To include this field in your subscription, you need permission to call ecs:ListClusters and ecs:ListTaskDefinitions Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-task-arn</td>
  <td>ARN of the ECS task if the traffic is from a running ECS task. To include this field in your subscription, you need permission to call ecs:ListClusters and ecs:ListTasks. Parquet data type: STRING</td>
  <td>7</td>
</tr>
<tr>
  <td>ecs-task-id</td>
  <td>ID of the ECS task if the traffic is from a running ECS task. To include this field in your subscription, you need permission to call ecs:ListClusters and ecs:ListTasks. Parquet data type: STRING</td>
  <td>7</td>
</tr>