from flow_log_analyzer import FlowLogAnalyzer


def main():
    analyzer = FlowLogAnalyzer('lookup_table.csv')
    port_protocol_counts, tag_counts = analyzer.parse_flow_logs('flow_logs.txt')
    analyzer.write_counts_to_file(tag_counts, port_protocol_counts, 'tag_counts.csv', 'port_protocol_counts.csv')



if __name__ == "__main__":
    main()
