import csv
#check word coverage
    #cover= ['access', 'add', 'address', 'allow']
cover=['access', 'add', 'address', 'allow', 'also', 'apiversion', 'app', 'application', 'apply', 'authentication', 'authorization', 'bookinfo', 'boolean', 'ca', 'certificate', 'client', 'cluster', 'clusters', 'command', 'config', 'configuration', 'configure', 'connection', 'context', 'control', 'create', 'curl', 'default', 'delete', 'deploy', 'deployment', 'description', 'destination', 'details', 'dns', 'docker', 'domain', 'egress', 'egressgateway', 'enabled', 'endpoints', 'envoy', 'eof', 'error', 'example', 'experimental', 'external', 'false', 'field', 'file', 'filter', 'flags', 'following', 'foo', 'gateway', 'gateways', 'get', 'host', 'hosts', 'http', 'httpbin', 'https', 'information', 'ingress', 'injection', 'install', 'installation', 'ip', 'istio', 'istioctl', 'istiod', 'key', 'kind', 'kubeconfig', 'kubectl', 'kubernetes', 'labels', 'level', 'list', 'load', 'log', 'match', 'mesh', 'message', 'metadata', 'metrics', 'mode', 'multiple', 'must', 'mutual', 'name', 'namespace', 'network', 'networkingistioiovalpha', 'new', 'nginx', 'number', 'one', 'operator', 'output', 'page', 'path', 'pilot', 'plane', 'pod', 'pods', 'policies', 'policy', 'port', 'ports', 'primary', 'prometheus', 'protocol', 'proxy', 'ratings', 'request', 'requests', 'required', 'resource', 'reviews', 'revision', 'route', 'routing', 'rule', 'rules', 'run', 'running', 'secret', 'see', 'selector', 'server', 'service', 'services', 'set', 'sidecar', 'single', 'sleep', 'sni', 'source', 'spec', 'specified', 'status', 'string', 'sum', 'system', 'task', 'tcp', 'test', 'time', 'tls', 'tokentracing', 'traffic', 'true', 'type', 'upgrade', 'use', 'used', 'using', 'value', 'verify', 'version', 'virtual', 'virtualservice', 'vm', 'without', 'workload', 'workloads']
for item in cover:
    print(item)
    counter=0
    with open('text.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            for field in row:
                if item in field:
                    counter=counter+1
        print(counter)