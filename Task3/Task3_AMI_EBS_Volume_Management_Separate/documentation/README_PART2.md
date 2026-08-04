# Part 2 — Prepare Ubuntu EC2 and Data Volume

[← Part 1](README_PART1.md) | [Next →](README_PART3.md)

## Launch Ubuntu EC2
```text
Name: project-03-source-ubuntu
AMI: Ubuntu Server 24.04 LTS
Type: t3.micro
Root: 8–10 GiB gp3
SSH: My IP only
```

```bash
chmod 400 project-key.pem
ssh -i project-key.pem ubuntu@<PUBLIC_IP>
```

## Create and Attach Data EBS
Create a 5 GiB gp3 volume in the **same AZ** as EC2, tag it `project-03-old-data-volume`, and attach it as `/dev/sdf`. On Nitro it normally appears as `/dev/nvme1n1`.

```bash
lsblk -f
sudo nvme list
sudo mkfs.ext4 /dev/nvme1n1
sudo mkdir -p /data
sudo mount /dev/nvme1n1 /data
echo 'Task 3 EBS verification file' | sudo tee /data/verification.txt
date | sudo tee -a /data/verification.txt
```

## Persistent Mount
```bash
sudo blkid /dev/nvme1n1
sudo cp /etc/fstab /etc/fstab.backup
```
Add:
```text
UUID=<UUID> /data ext4 defaults,nofail 0 2
```
Validate:
```bash
sudo umount /data
sudo mount -a
df -hT
```
