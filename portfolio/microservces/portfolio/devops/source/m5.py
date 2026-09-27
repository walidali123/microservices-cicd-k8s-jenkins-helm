from lib import *
FOOT = "Based strictly on repository configuration · microservices-projects"
OUT = "/home/claude/p3/portfolio/devops/"
d = Diagram("DevOps Case Study · Security",
            "Security & Access Configuration",
            "Encrypted entry through the Ingress, private services and registry, and credentials kept outside the pipeline code", FOOT)

d.zone(80, 250, 1760, 225, "Request path", "sec", fill="#FFFFFF00")
y, h = 290, 150
d.node(110, y, 230, h, "src", "user", "Shopper", "Browser request")
d.node(430, y, 330, h, "proxy", "lock", "NGINX Ingress", "TLS on the shop host", chips=["tls: secretName"])
d.zone(850, 282, 970, 168, "Namespace kart · ClusterIP only", "proxy", fill="#F0FDF8")
for x, c, ic, t in [(870, "web", "globe", "client"), (1105, "api", "code", "main API"), (1340, "api", "code", "books API"), (1575, "db", "db", "databases")]:
    d.node(x, 302, 220, 128, c, ic, t, "")
m = y + h // 2
d.arrow([(340, m), (426, m)], color="#059669"); d.pill(383, m - 30, "https", "proxy")
d.arrow([(760, m), (866, m)], color="#059669"); d.pill(813, m - 30, "routes", "proxy")

cards = [
    ("proxy", "lock", "TLS at the edge", "The storefront Ingress terminates HTTPS using a certificate stored as a Kubernetes TLS secret.", ["ingressClassName: nginx", "tls.secretName"]),
    ("proxy", "net", "Private services", "Every Service is ClusterIP. Apps and databases are reachable only inside the cluster, behind the Ingress.", ["5 × ClusterIP", "Ingress-only exposure"]),
    ("reg", "layers", "Private image registry", "Images live in a private Nexus registry and are pulled with an image pull secret.", ["imagePullSecrets: regcred"]),
    ("sec", "key", "Pipeline credentials", "Jenkins references registry login and cluster access by credential ID. No kubeconfig is stored in the repo.", ["NexusRepoLogin", "kubeconfig (file)"]),
    ("db", "db", "Database credentials", "The MySQL root password is read from a Kubernetes Secret, and DB names from a ConfigMap.", ["secretKeyRef", "configMapKeyRef"]),
    ("ci", "check", "Traceable releases", "Each image is tagged with the Jenkins build number, so every running pod maps to a specific build.", [":$BUILD_NUMBER"]),
]
for i, (c, ic, t, s, ch) in enumerate(cards):
    cx = 80 + (i % 3) * 600; cy = 515 + (i // 3) * 235
    d.node(cx, cy, 560, 215, c, ic, t, s, chips=ch)
d.render(OUT + "05-security.png")
