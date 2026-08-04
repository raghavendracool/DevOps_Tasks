# Part 3 — Create and Copy the AMI

[← Part 2](README_PART2.md) | [Next →](README_PART4.md)

## Create Source AMI
```bash
sudo sync
df -hT
lsblk -f
```
In EC2 Console: **Instances → Actions → Image and templates → Create image**.

```text
Name: project-03-ubuntu-ami
Reboot: Allow reboot for filesystem consistency
```
Wait until the AMI state is `Available`.

## Copy to Another Region
Select the AMI → **Actions → Copy AMI**.

```text
Destination: us-east-1
Name: project-03-ubuntu-ami-copy
```
Switch to the destination Region and wait for `Available`.

## Launch from Copied AMI
Use a destination-region key pair, subnet and Security Group. Launch `t3.micro`, connect, and verify:
```bash
cat /etc/os-release
lsblk -f
df -hT
```

> AMI IDs, key pairs, Security Groups, VPCs and subnets are Region-specific.
