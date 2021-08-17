from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

API_BASE_URL = "http://0.0.0.0:80"

kubeconfig = '''{\r\n    \"baseType\": \"generateKubeConfigOutput\",\r\n    \"config\": \"apiVersion: v1\\nkind: Config\\nclusters:\\n- name: \\\"k8s-cluster\\\"\\n  cluster:\\n    server: \\\"https:\/\/rancher-preprodna.10006.elluciancloud.com\/k8s\/clusters\/c-r7jkr\\\"\\n- name: \\\"k8s-cluster-fqdn\\\"\\n  cluster:\\n    server: \\\"https:\/\/k8s-cluster.kubetesting1.test.elluciancloud.com:6443\\\"\\n\\nusers:\\n- name: \\\"k8s-cluster\\\"\\n  user:\\n    token: \\\"kubeconfig-u-xjcen4jget.c-r7jkr:kpxtfvt9lnv5jgbfjkd6hzhcpr6sdfesbdcvjkt2nfwh4v5blp9wsk\\\"\\n\\n\\ncontexts:\\n- name: \\\"k8s-cluster\\\"\\n  context:\\n    user: \\\"k8s-cluster\\\"\\n    cluster: \\\"k8s-cluster\\\"\\n- name: \\\"k8s-cluster-fqdn\\\"\\n  context:\\n    user: \\\"k8s-cluster\\\"\\n    cluster: \\\"k8s-cluster-fqdn\\\"\\n\\ncurrent-context: \\\"k8s-cluster\\\"\\n\",\r\n    \"type\": \"generateKubeConfigOutput\"\r\n\r\n}'''


class HTTPHandler(BaseHTTPRequestHandler):
    called = False
    bearer_header_found = False

    def do_HEAD(self):
        self.send_response(200)

    def do_GET(self):
        HTTPHandler.called = True
        HTTPHandler.bearer_header_found = any(
            k for k in self.headers if k == "authorization" and self.headers[k] == "Bearer secret")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(kubeconfig.encode("utf-8"))

    def do_POST(self):
        HTTPHandler.called = True
        HTTPHandler.bearer_header_found = any(
            k for k in self.headers if k == "authorization" and self.headers[k] == "Bearer secret")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(kubeconfig.encode("utf-8"))


server_address = urlparse(API_BASE_URL)
with HTTPServer((server_address.hostname, server_address.port), HTTPHandler) as httpd:
    httpd.serve_forever()
