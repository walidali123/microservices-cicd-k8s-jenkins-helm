from lib import *
FOOT = "Based strictly on repository configuration · microservices-projects"
OUT = "/home/claude/p3/portfolio/devops/"
d = Diagram("DevOps Case Study · Infrastructure",
            "Helm Umbrella Chart: What Runs in the Cluster",
            "One release deploys three subcharts (frontend, backend and database) into the kart namespace", FOOT)

d.zone(80, 245, 1760, 745, "Helm umbrella chart · kkartcharts 1.1.0", "ci", dashed=False, fill="#FCFCFF",
       note="helm upgrade kubekart kkartchart --install -n kart")
cols = [(115, "kkartcharts-frontend", "web"), (690, "kkartcharts-backend", "api"), (1265, "kkartcharts-database", "db")]
for x, name, c in cols:
    d.zone(x, 300, 540, 665, f"Subchart · {name}", c, fill="#FFFFFF")
W = 480
def col(x, cards, top=340, bottom=940, gap=16):
    h = (bottom - top - gap * (len(cards) - 1)) // len(cards)
    for i, (c, ic, t, s, ch) in enumerate(cards):
        d.node(x + 30, top + i * (h + gap), W, h, c, ic, t, s, chips=ch)

col(115, [
    ("proxy", "shield", "Ingress · storefront", "Serves the shop domain over TLS", ["class: nginx", "TLS secret", "path: /"]),
    ("web", "globe", "client", "Angular build served by Nginx", ["Deployment", "ClusterIP :4200"]),
    ("reg", "lock", "Private image pulls", "Images are pulled from Nexus on every rollout", ["imagePullSecrets: regcred", "pullPolicy: Always"]),
])
col(690, [
    ("proxy", "shield", "Ingress · APIs", "Routes API paths on the same host", ["/api → main", "/webapi → books"]),
    ("api", "code", "main · Node.js API", "Connects to MongoDB as emongo", ["Deployment", "ClusterIP :5000"]),
    ("api", "code", "books · Java API", "Spring Boot, connects to MySQL as emartdb", ["Deployment", "ClusterIP :9000"]),
])
col(1265, [
    ("db", "db", "MongoDB", "Reached by the Node.js API as emongo", ["mongo:4", ":27017", "/data/db"]),
    ("db", "db", "MySQL", "Reached by the Java API as emartdb", ["mysql:5.7.25", ":3306", "/var/lib/mysql"]),
    ("sec", "key", "ConfigMap + Secret", "DB names and root password injected", ["configMapKeyRef", "secretKeyRef"]),
    ("store", "disk", "PersistentVolumeClaims ×2", "One claim per database on NFS storage", ["500Mi · RWX", "pod-nfs-storage"]),
])

d.legend([("proxy", "Ingress"), ("web", "Frontend"), ("api", "APIs"), ("db", "Databases"), ("sec", "Config & secrets"),
          ("reg", "Registry access"), ("store", "Storage")], y=1012)
d.render(OUT + "03-infrastructure.png")
