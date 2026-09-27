from lib import *
FOOT = "Based strictly on repository configuration · microservices-projects"
OUT = "/home/claude/p3/portfolio/devops/"
d = Diagram("DevOps Case Study · CI/CD",
            "Jenkins Monorepo Pipeline: Build, Publish, Deploy",
            "Each service has its own build → push → deploy lane, and a lane runs only when files in that service change", FOOT)

d.node(80, 290, 300, 165, "src", "branch", "Code Change", "Commit to the monorepo", chips=["Jenkinsfile"])
d.node(80, 500, 300, 215, "ci", "net", "Changeset Router", "Each lane is gated by the folder that changed",
       chips=["when { changeset }"])
d.arrow([(230, 455), (230, 496)])
d.node(80, 760, 300, 225, "sec", "key", "Jenkins Credentials", "Stored in Jenkins and referenced by ID",
       chips=["NexusRepoLogin", "kubeconfig file"])

lanes = [
    (245, "Lane 1 · Angular client", "client/*", [
        ("reg", "cube", "Build image", "docker.build from ./client", ["client:$BUILD_NUMBER"]),
        ("reg", "layers", "Push to Nexus", "Tags the build number and latest", ["docker.withRegistry"]),
        ("ci", "terminal", "Helm deploy", "Upgrades only the frontend image tag", ["frontend.image.client.tag"]),
    ]),
    (505, "Lane 2 · Java Books API", "javaapi/*", [
        ("reg", "cube", "Build image", "docker.build from ./javaapi", ["books:$BUILD_NUMBER"]),
        ("reg", "layers", "Push to Nexus", "Tags the build number and latest", ["docker.withRegistry"]),
        ("ci", "terminal", "Helm deploy", "Upgrades only the books image tag", ["backend.image.books.tag"]),
    ]),
    (765, "Lane 3 · Node.js API", "nodeapi/*", [
        ("sec", "file", "Set DB host", "Points config at the in-cluster MongoDB", ["localhost → emongo"]),
        ("reg", "cube", "Build image", "docker.build from ./nodeapi", ["main:$BUILD_NUMBER"]),
        ("reg", "layers", "Push to Nexus", "Build number and latest", ["docker.withRegistry"]),
        ("ci", "terminal", "Helm deploy", "Upgrades the main image tag", ["backend.image.main.tag"]),
    ]),
]
for ly, label, gate, steps in lanes:
    d.zone(440, ly, 1400, 220, label, "ci", fill="#FFFFFF", note=f"runs when {gate} changes")
    n = len(steps); gap = 50
    w = (1340 - gap * (n - 1)) // n
    xs = [470 + i * (w + gap) for i in range(n)]
    for x, (c, ic, t, s, ch) in zip(xs, steps):
        d.node(x, ly + 38, w, 160, c, ic, t, s, chips=ch)
    m = ly + 38 + 80
    for a in xs[:-1]:
        d.arrow([(a + w, m), (a + w + gap - 4, m)])
    d.arrow([(380, 607), (412, 607), (412, m), (466, m)], color="#4F46E5")

d.render(OUT + "02-cicd-pipeline.png")
