from lib import *
FOOT = "Based strictly on repository configuration · microservices-projects"
OUT = "/home/claude/p3/portfolio/devops/"
d = Diagram("DevOps Case Study · Architecture",
            "Microservices CI/CD to Kubernetes with Jenkins, Nexus & Helm",
            "Only the changed service is rebuilt, versioned in a private registry and rolled out to the cluster with Helm", FOOT)

d.zone(80, 235, 1760, 245, "Build & delivery · automated", "ci")
y, h = 270, 180
d.node(120, y, 250, h, "src", "user", "Developer", "Pushes changes to any service folder")
d.node(470, y, 380, h, "src", "branch", "Git Monorepo", "Three services plus deployment chart",
       chips=["client/", "nodeapi/", "javaapi/", "kkartchart/"])
d.node(950, y, 400, h, "ci", "play", "Jenkins Pipeline", "Detects which service changed and builds only that one",
       chips=["changeset stages", "Docker build"])
d.node(1450, y, 350, h, "reg", "layers", "Nexus Registry", "Private Docker registry, versioned images",
       chips=[":BUILD_NUMBER", ":latest"])
my = y + h // 2
d.arrow([(370, my), (466, my)]); d.pill(418, my - 30, "git push")
d.arrow([(850, my), (946, my)]); d.pill(898, my - 30, "changes")
d.arrow([(1350, my), (1446, my)]); d.pill(1398, my - 30, "push")

d.zone(400, 560, 1440, 430, "Kubernetes cluster · namespace kart", "proxy", note="deployed as Helm release kubekart")
rows = [600, 732, 864]; rh = 112
d.node(440, 670, 270, 230, "proxy", "shield", "NGINX Ingress", "Single entry point with TLS and path-based routing",
       chips=["TLS", "host rule"])
d.node(800, rows[0], 320, rh, "web", "globe", "Angular Client", "", chips=["nginx · :4200"])
d.node(800, rows[1], 320, rh, "api", "code", "Node.js API", "", chips=["main · :5000"])
d.node(800, rows[2], 320, rh, "api", "code", "Java Books API", "", chips=["Spring Boot · :9000"])
d.node(1210, rows[1], 270, rh, "db", "db", "MongoDB", "", chips=["emongo · :27017"])
d.node(1210, rows[2], 270, rh, "db", "db", "MySQL", "", chips=["emartdb · :3306"])
d.node(1570, 732, 240, 244, "store", "disk", "Persistent Volumes", "One claim per database on NFS-backed storage",
       chips=["PVC ×2", "500Mi each"])

for r, lbl in zip(rows, ["/", "/api", "/webapi"]):
    m = r + rh // 2
    d.arrow([(710, 785), (750, 785), (750, m), (796, m)], color="#059669")
    d.pill(772, m - 22, lbl, "proxy", mono=True)
for r in rows[1:]:
    m = r + rh // 2
    d.arrow([(1120, m), (1206, m)])
    d.arrow([(1480, m), (1566, m)], color="#94A3B8", dashed=True)

d.node(100, 700, 230, 170, "src", "user", "Shoppers", "Web browser", center=True)
d.arrow([(330, 785), (436, 785)], color="#059669"); d.pill(383, 755, "HTTPS", "proxy")

d.arrow([(1150, 450), (1150, 556)], color="#4F46E5"); d.pill(1150, 518, "helm upgrade --install", "ci", mono=True)
d.arrow([(1625, 450), (1625, 556)], color="#0284C7", dashed=True); d.pill(1625, 518, "image pull", "reg")

d.legend([("src", "Source"), ("ci", "CI/CD"), ("reg", "Registry"), ("proxy", "Ingress"),
          ("web", "Frontend"), ("api", "APIs"), ("db", "Databases"), ("store", "Storage")], y=1012)
d.render(OUT + "01-devops-architecture.png")
