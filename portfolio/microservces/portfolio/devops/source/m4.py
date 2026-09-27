from lib import *
FOOT = "Based strictly on repository configuration · microservices-projects"
OUT = "/home/claude/p3/portfolio/devops/"
d = Diagram("DevOps Case Study · Deployment Flow",
            "How a Code Change Reaches the Cluster",
            "Every release is traceable to a Jenkins build number, from image tag to running pod", FOOT)

n = 6; gap = 44; w = (1760 - gap * (n - 1)) // n
xs = [80 + i * (w + gap) for i in range(n)]
steps = [
    ("src", "branch", "Commit", "Change pushed in one service folder", ["git push"]),
    ("ci", "net", "Detect", "Changeset rule picks the matching lane", ["when { changeset }"]),
    ("reg", "cube", "Build", "Docker image built and tagged", [":$BUILD_NUMBER"]),
    ("reg", "layers", "Publish", "Pushed to the private Nexus registry", [":BUILD_NUMBER", ":latest"]),
    ("ci", "terminal", "Upgrade", "Helm sets the new tag for that service only", ["helm upgrade --install"]),
    ("proxy", "globe", "Roll out", "New pod pulls the image and serves via Ingress", ["regcred", "Ingress"]),
]
d.zone(55, 265, 1810, 320, "Release path · automated by Jenkins", "ci", fill="#FFFFFF00", note="namespace: kart")
for i, (x, (c, ic, t, s, ch)) in enumerate(zip(xs, steps)):
    d.node(x, 310, w, 235, c, ic, f"<span style='color:{C[c][0]};font-weight:800'>{i+1:02d}</span>&nbsp; {t}", s, chips=ch)
for a in xs[:-1]:
    d.arrow([(a + w, 427), (a + w + gap - 4, 427)])

# local environment
d.zone(55, 660, 1810, 320, "Local environment · Docker Compose", "proxy", fill="#FFFFFF00", note="docker-compose.yaml")
ly, lh = 705, 235
d.node(80, ly, 330, lh, "src", "terminal", "Compose up", "Builds the three service images from their Dockerfiles",
       ["docker compose up --build"])
d.node(470, ly, 360, lh, "proxy", "shield", "Nginx API Gateway", "Single entry on port 80 with path-based routing",
       ["/", "/api", "/webapi"])
d.node(890, ly, 480, lh, "api", "code", "Service containers", "Angular client, Node.js API and Java Books API",
       ["client :4200", "api :5000", "webapi :9000"])
d.node(1430, ly, 410, lh, "db", "db", "Database containers", "Same hostnames the cluster uses",
       ["emongo · mongo:4", "emartdb · mysql:8.0.33"])
m = ly + lh // 2
d.arrow([(410, m), (466, m)]); d.arrow([(830, m), (886, m)]); d.arrow([(1370, m), (1426, m)])

d.text(80, 1003, 1500, "Local routing mirrors the cluster Ingress: <span class='mono'>/</span> → client, <span class='mono'>/api</span> → Node.js API, <span class='mono'>/webapi</span> → Java API.", 15, "#64748B", 500)
d.render(OUT + "04-deployment-flow.png")
