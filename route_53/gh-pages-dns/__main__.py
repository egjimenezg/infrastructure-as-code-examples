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

github_pages_aaaa = [
  "2606:50c0:8000::153",
  "2606:50c0:8001::153",
  "2606:50c0:8002::153",
  "2606:50c0:8003::153",
]

config = pulumi.Config()

domain = config.require("domain")

gh_pages_target = config.require("githubPagesTarget")

zone = aws.route53.Zone(
  "primary-zone",
  name=domain
)

zone_id = zone.zone_id

aws.route53.Record(
  "apex-a",
  zone_id=zone_id,
  name=domain,
  type="A",
  ttl=300,
  records=github_pages_a
)

aws.route53.Record(
  "apex-aaaa",
  zone_id=zone.zone_id,
  name=domain,
  type="AAAA",
  ttl=300,
  records=github_pages_aaaa
)

aws.route53.Record(
  "www-cname",
  zone_id=zone_id,
  name=f"www.{domain}",
  type="CNAME",
  ttl=300,
  records=[gh_pages_target]
)

pulumi.export("zoneId", zone_id)
pulumi.export("domain", domain)
pulumi.export("www", f"www.{domain}")
