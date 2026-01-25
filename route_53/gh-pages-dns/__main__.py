"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# See: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-an-apex-domain
github_pages_a = [
  "185.199.108.153",
  "185.199.109.153",
  "185.199.110.153",
  "185.199.111.153"
]

config = pulumi.Config()

domain = config.require("domain")

gh_pages_target = config.require("githubPagesTarget")

zone = aws.route53.get_zone(name=domain.rstrip(".") + ".", private_zone=False)
zone_id = zone.zone_id

aws.route53.Record(
  "apex-a",
  zone_id=zone_id,
  name=domain,
  type="A",
  ttl=300,
  records=github_pages_a
)

pulumi.export("zoneId", zone_id)
pulumi.export("domain", domain)
