import csv
import logging
logging.basicConfig(level=logging.INFO)


class FlowLogAnalyzer:
    """
    Analyzes network flow logs to identify and count occurrences of port-protocol combinations and associated tags.

    This class provides functionality to load a lookup table from a CSV file, parse flow log files to extract
    information about destination ports and protocols, map these to human-readable protocol names and predefined
    tags, and count the occurrences of each port-protocol combination and tag. It also supports writing these
    counts to CSV files for further analysis.

    Attributes:
        lookup_table (dict): A dictionary mapping (dstport, protocol) tuples to tags, loaded from a CSV file.
        protocol_mapping (dict): A predefined mapping of protocol numbers to human-readable names.
    """

    def __init__(self, lookup_table_filename):
        """
        Initializes the analyzer with a lookup table and a predefined protocol mapping.

        This constructor loads a lookup table from a specified file and sets up a basic
        protocol mapping that translates protocol numbers into human-readable protocol names.

        Args:
            lookup_table_filename (str): The path to the file containing the lookup table data.
        """
        self.lookup_table = self.load_lookup_table(lookup_table_filename)
        self.protocol_mapping = {'6': 'tcp', '17': 'udp', '1': 'icmp'}

    def load_lookup_table(self, filename):
        """
        Loads a lookup table from a CSV file.
        Reads a CSV file to construct a lookup table where keys are (dstport, protocol) tuples,
        and values are tags. Handles missing tags by defaulting to an unknown tag. Logs warnings
        for missing columns and errors for file or read issues.

        Args:
            filename (str): Path to the CSV file.

        Returns:
            dict: Lookup table mapping (dstport, protocol) to tags.

        Raises:
            FileNotFoundError: If the CSV file cannot be found.
        """
        lookup_table = {}
        try:
            with open(filename, mode='r', newline='') as csvfile:
                reader = csv.DictReader((line.strip() for line in csvfile))
                for row in reader:
                    try:
                        key = (row['dstport'].strip(),
                               row['protocol'].strip().lower())
                        lookup_table[key] = row.get('tag', 'unknown').strip()
                    except KeyError as e:
                        logging.warning(
                            f"""Missing expected column in CSV row: {e}""")
            logging.info(
                f"""Lookup table loaded successfully from {filename} with {len(lookup_table)} tags.""")
        except FileNotFoundError:
            logging.error(f"""File not found: {filename}""")
            raise
        except csv.Error as e:
            logging.error(f"""Error reading CSV file {filename}: {e}""")
        except Exception as e:
            logging.error(f"""Unexpected error loading lookup table from {
                          filename}: {e}""")
        return lookup_table

    def parse_flow_logs(self, filename):
        """
        Parses flow log files to count occurrences of port-protocol combinations and tags.

        This method reads a flow log file line by line, extracting destination port and protocol
        numbers, mapping them to protocol names, and counting their occurrences. It also maps
        each port-protocol pair to a tag using a lookup table and counts tag occurrences.
        ICMP protocol is handled specially by setting destination port to '0'.

        Args:
            filename (str): The path to the flow log file.
        Returns:
            tuple of (dict, dict): A tuple containing two dictionaries:
                - The first dictionary maps (dstport, protocol) tuples to their counts.
                - The second dictionary maps tags to their counts.

        Raises:
            FileNotFoundError: If the log file cannot be found.

        """
        port_protocol_counts = {}
        tag_counts = {}
        log_count = 0
        successful_logs_count = 0
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                for line in file:
                    log_count += 1
                    try:
                        parts = line.split()
                        if len(parts) < 8:
                            logging.warning(f"""Invalid log line: {line}""")
                            continue
                        successful_logs_count += 1
                        dstport = parts[6]
                        protocol_num = parts[7]
                        protocol = self.protocol_mapping.get(
                            protocol_num, 'unknown').lower()

                        if protocol == 'icmp':
                            dstport = '0'

                        key = (dstport, protocol)
                        port_protocol_counts[key] = port_protocol_counts.get(
                            key, 0) + 1
                        tag = self.lookup_table.get(key, 'Untagged')
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
                    except IndexError as e:
                        logging.error(
                            f"""Error processing line '{line}': {e}""")
            logging.info(
                f"""Loaded flow logs from {filename}. Found {log_count} logs, successfully processed {successful_logs_count} logs.""")
        except FileNotFoundError:
            logging.error(f"""Flow log file not found: {filename}""")
            raise
        except Exception as e:
            logging.error(f"""Unexpected error parsing flow logs from {
                          filename}: {e}""")
        return port_protocol_counts, tag_counts

    def write_counts_to_file(self, tag_counts, port_protocol_counts, tag_filename, port_protocol_filename):
        """
        Writes the counts of tags and port-protocol pairs to specified CSV files.

        This method takes dictionaries of tag counts and port-protocol counts, then writes them
        to separate CSV files.
        Tag file contains two columns: Tag, Count columns
        Port protocol file contains Port, Protocol, Count columns.

        Args:
            tag_counts (dict): A dictionary mapping tags to their counts.
            port_protocol_counts (dict): A dictionary mapping (port, protocol) tuples to their counts.
            tag_filename (str): The filename for the CSV file to write tag counts.
            port_protocol_filename (str): The filename for the CSV file to write port-protocol counts.

        Raises:
            Exception: If an error occurs while writing to the files.
        """
        try:
            with open(tag_filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Tag', 'Count'])
                for tag, count in tag_counts.items():
                    writer.writerow([tag, count])

            with open(port_protocol_filename, mode='w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Port', 'Protocol', 'Count'])
                for (port, protocol), count in port_protocol_counts.items():
                    writer.writerow([port, protocol, count])
            logging.info(f"""Successfully analyzed and added Tag Counts to file: {
                         tag_filename} and Port/Protocol Counts to file: {port_protocol_filename}.""")

        except Exception as e:
            logging.error(f"""Failed to write counts to file: {e}""")
