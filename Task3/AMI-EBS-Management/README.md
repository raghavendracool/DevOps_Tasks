# AWS Project 3: Amazon Machine Image (AMI) and EBS Volume Management

![Task 3 Full Infographic](images/task-03-full-infographic.png)

## Objective

This project demonstrates how to:

- Launch an Ubuntu EC2 instance and configure NGINX.
- Attach and mount a non-root Amazon EBS volume.
- Create an AMI from the EC2 instance.
- Copy the AMI to another AWS Region.
- Create a snapshot of the data volume.
- Replace the old EBS volume with a new volume created from the snapshot.
- Validate the restored data and persistent mount.
- Delete the old volume only after successful verification.

---

## Architecture

![Architecture Overview](images/01-architecture-overview.png)

![AMI Workflow](images/02-ami-workflow.png)

![EBS Replacement Workflow](images/03-ebs-replacement-workflow.png)

![Ubuntu Commands](images/04-ubuntu-command-reference.png)

---

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon EC2 | Ubuntu web server |
| Amazon EBS | Root and data storage |
| EBS Snapshot | Point-in-time backup of the data volume |
| Amazon Machine Image | Reusable EC2 machine image |
| Amazon VPC | Networking |
| Security Group | SSH and HTTP access |
| AWS IAM | Permissions |

---

## Example Lab Values

| Setting | Value |
|---|---|
| Source Region | `ap-south-1` |
| Destination Region | `us-east-1` |
| EC2 Name | `task3-ami-ebs-server` |
| OS | Ubuntu Server 24.04 LTS |
| Instance Type | `t3.micro` |
| Root Volume | 8 GiB gp3 |
| Data Volume | 5 GiB gp3 |
| Mount Point | `/data` |
| AMI Name | `task3-ubuntu-nginx-ami` |

Replace these values based on your AWS account.

---

# Part 1: Launch the Ubuntu EC2 Instance

1. Open **AWS Console → EC2 → Instances → Launch instances**.
2. Configure:

```text
Name: task3-ami-ebs-server
AMI: Ubuntu Server 24.04 LTS
Instance type: t3.micro
Key pair: Select or create one
Public IP: Enabled
```

3. Configure security-group inbound rules:

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | My IP |
| HTTP | 80 | `0.0.0.0/0` |

4. Keep the default root volume or use `8 GiB gp3`.
5. Launch the instance.

Connect:

```bash
chmod 400 task3-key.pem
ssh -i task3-key.pem ubuntu@<EC2_PUBLIC_IP>
```

---

# Part 2: Install NGINX

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install nginx -y
sudo systemctl enable --now nginx
sudo systemctl status nginx
```

Create a simple page:

```bash
sudo tee /var/www/html/index.html > /dev/null <<'EOF'
<!DOCTYPE html>
<html>
<head>
  <title>AMI and EBS Project</title>
</head>
<body>
  <h1>AWS AMI and EBS Management</h1>
  <p>This page is hosted from an Ubuntu EC2 instance.</p>
</body>
</html>
EOF
```

Verify:

```text
http://<EC2_PUBLIC_IP>
```

---

# Part 3: Create and Attach the Original Data Volume

1. Note the EC2 instance Availability Zone from the instance details.
2. Open **EC2 → Volumes → Create volume**.
3. Configure:

```text
Type: gp3
Size: 5 GiB
Availability Zone: Same AZ as the EC2 instance
Encryption: Enabled
Tag Name: task3-original-data-volume
```

4. Select the volume.
5. Choose **Actions → Attach volume**.
6. Select the EC2 instance.
7. Use device name `/dev/sdf`.

On Nitro-based instances, `/dev/sdf` may appear as `/dev/nvme1n1`.

Check:

```bash
lsblk
sudo file -s /dev/nvme1n1
```

Format only the new empty volume:

```bash
sudo mkfs.ext4 /dev/nvme1n1
```

Create a mount point and mount it:

```bash
sudo mkdir -p /data
sudo mount /dev/nvme1n1 /data
df -hT /data
```

Create test data:

```bash
sudo mkdir -p /data/project-files
echo "This data is stored on the original EBS volume." | \
sudo tee /data/project-files/ebs-test.txt
date | sudo tee -a /data/project-files/ebs-test.txt
cat /data/project-files/ebs-test.txt
```

Configure persistent mounting:

```bash
sudo blkid /dev/nvme1n1
sudo cp /etc/fstab /etc/fstab.backup
```

Add the actual UUID to `/etc/fstab`:

```text
UUID=<ACTUAL_UUID> /data ext4 defaults,nofail 0 2
```

Test:

```bash
sudo mount -a
df -hT /data
```

---

# Part 4: Create an AMI

1. Open **EC2 → Instances**.
2. Select `task3-ami-ebs-server`.
3. Choose **Actions → Image and templates → Create image**.
4. Configure:

```text
Image name: task3-ubuntu-nginx-ami
Description: Ubuntu NGINX server for Task 3
```

5. Keep reboot enabled for filesystem consistency.
6. Create the image.
7. Open **EC2 → AMIs** and wait until the status is `Available`.

AWS creates backing snapshots for the EBS volumes included in the AMI.

## Test the AMI

1. Select the new AMI.
2. Choose **Launch instance from AMI**.
3. Launch a temporary `t3.micro`.
4. Allow SSH and HTTP.
5. Verify the NGINX page.

Terminate the temporary instance after testing.

---

# Part 5: Copy the AMI to Another Region

1. In the source Region, open **EC2 → AMIs**.
2. Select `task3-ubuntu-nginx-ami`.
3. Choose **Actions → Copy AMI**.
4. Configure:

```text
Destination Region: us-east-1
Name: task3-ubuntu-nginx-ami-us-east-1
```

5. Start the copy.
6. Switch to `us-east-1`.
7. Open **EC2 → AMIs**.
8. Wait for the copied AMI to become `Available`.

The copied AMI receives a new AMI ID because AMIs are Regional resources.

Optional AWS CLI:

```bash
aws ec2 copy-image \
  --source-region ap-south-1 \
  --source-image-id ami-REPLACE_ME \
  --region us-east-1 \
  --name "task3-ubuntu-nginx-ami-us-east-1"
```

---

# Part 6: Snapshot the Original Data Volume

Flush pending writes:

```bash
sync
```

In the AWS Console:

1. Open **EC2 → Volumes**.
2. Select `task3-original-data-volume`.
3. Choose **Actions → Create snapshot**.
4. Add:

```text
Description: Snapshot before replacing Task 3 data volume
Name: task3-original-data-snapshot
```

5. Wait until the snapshot status is `Completed`.

---

# Part 7: Create the Replacement Volume

1. Open **EC2 → Snapshots**.
2. Select `task3-original-data-snapshot`.
3. Choose **Actions → Create volume from snapshot**.
4. Configure:

```text
Type: gp3
Size: 5 GiB or larger
Availability Zone: Same AZ as the EC2 instance
Encryption: Enabled
Name: task3-new-data-volume
```

5. Wait until the volume state is `Available`.

Important: a volume created from the snapshot already contains the filesystem and files. Do not run `mkfs` on it.

---

# Part 8: Safely Detach the Old Volume

Record the current configuration:

```bash
lsblk -f
df -hT /data
sudo blkid
cat /data/project-files/ebs-test.txt
```

Flush and unmount:

```bash
sync
cd /
sudo umount /data
findmnt /data
```

If the device is busy:

```bash
sudo lsof +f -- /data
sudo fuser -vm /data
```

Temporarily comment the `/data` entry in `/etc/fstab`, then test:

```bash
sudo mount -a
```

In the AWS Console:

1. Open **EC2 → Volumes**.
2. Select the old volume.
3. Choose **Actions → Detach volume**.
4. Wait until its state becomes `Available`.

Do not delete it yet.

---

# Part 9: Attach and Mount the New Volume

1. Select `task3-new-data-volume`.
2. Choose **Actions → Attach volume**.
3. Select the original EC2 instance.
4. Use `/dev/sdf`.

On Ubuntu, identify the actual device:

```bash
lsblk -f
sudo blkid
```

Mount it using the real NVMe name:

```bash
sudo mount /dev/nvme1n1 /data
```

Verify the original data:

```bash
ls -la /data/project-files
cat /data/project-files/ebs-test.txt
```

Test write access:

```bash
echo "Replacement volume validation successful." | \
sudo tee /data/project-files/new-volume-test.txt

cat /data/project-files/new-volume-test.txt
df -hT /data
```

Restore the persistent mount entry in `/etc/fstab`:

```text
UUID=<REPLACEMENT_VOLUME_UUID> /data ext4 defaults,nofail 0 2
```

Test:

```bash
sudo umount /data
sudo mount -a
findmnt /data
df -hT /data
```

---

# Part 10: Reboot Validation

```bash
sudo reboot
```

Reconnect and verify:

```bash
findmnt /data
df -hT /data
cat /data/project-files/ebs-test.txt
cat /data/project-files/new-volume-test.txt
sudo systemctl status nginx
```

Verify the website again:

```text
http://<EC2_PUBLIC_IP>
```

---

# Part 11: Delete the Old Volume

Delete the old volume only after confirming:

- New volume is attached.
- `/data` is mounted.
- Original files exist.
- New files can be created.
- Mount survives reboot.
- NGINX is running.
- Old volume is detached and in `Available` state.

Then:

1. Open **EC2 → Volumes**.
2. Select the old volume.
3. Choose **Actions → Delete volume**.
4. Confirm deletion.

---

# Useful AWS CLI Commands

Set variables:

```bash
export AWS_REGION="ap-south-1"
export DESTINATION_REGION="us-east-1"
export INSTANCE_ID="i-REPLACE_ME"
export OLD_VOLUME_ID="vol-REPLACE_ME"
export NEW_VOLUME_ID="vol-REPLACE_ME"
export SOURCE_AMI_ID="ami-REPLACE_ME"
```

Create AMI:

```bash
aws ec2 create-image \
  --instance-id "$INSTANCE_ID" \
  --name "task3-ubuntu-nginx-ami" \
  --description "Ubuntu NGINX AMI for Task 3" \
  --region "$AWS_REGION"
```

List owned AMIs:

```bash
aws ec2 describe-images \
  --owners self \
  --region "$AWS_REGION" \
  --query 'Images[*].[ImageId,Name,State,CreationDate]' \
  --output table
```

Detach old volume:

```bash
aws ec2 detach-volume \
  --volume-id "$OLD_VOLUME_ID" \
  --region "$AWS_REGION"
```

Attach new volume:

```bash
aws ec2 attach-volume \
  --volume-id "$NEW_VOLUME_ID" \
  --instance-id "$INSTANCE_ID" \
  --device /dev/sdf \
  --region "$AWS_REGION"
```

Delete old volume:

```bash
aws ec2 delete-volume \
  --volume-id "$OLD_VOLUME_ID" \
  --region "$AWS_REGION"
```

---

# Troubleshooting

## `/dev/sdf` is not shown

Nitro instances expose EBS devices as NVMe devices.

```bash
lsblk
sudo apt update
sudo apt install nvme-cli -y
sudo nvme list
```

## Volume cannot be attached

The EBS volume and EC2 instance must be in the same Availability Zone.

## `umount: target is busy`

```bash
cd /
sudo lsof +f -- /data
sudo fuser -vm /data
sudo umount /data
```

## Wrong filesystem type

```bash
sudo file -s /dev/nvme1n1
sudo blkid /dev/nvme1n1
```

Do not format an existing or snapshot-restored volume unless you intend to erase it.

## EC2 boot issue after `/etc/fstab` changes

Use `nofail` and always test before reboot:

```bash
sudo mount -a
```

## Duplicate filesystem UUID

A snapshot-restored volume usually retains the original filesystem UUID. Avoid attaching both copies simultaneously with the same `/etc/fstab` UUID entry.

---

# Validation Checklist

- [ ] Ubuntu EC2 instance is running.
- [ ] NGINX is active.
- [ ] Website is accessible.
- [ ] Original data EBS volume is mounted at `/data`.
- [ ] Test data is created.
- [ ] Custom AMI is `Available`.
- [ ] AMI test instance works.
- [ ] Copied AMI is `Available` in the destination Region.
- [ ] EBS snapshot is `Completed`.
- [ ] Replacement volume is created in the same AZ.
- [ ] Old volume is safely unmounted and detached.
- [ ] Replacement volume is attached and mounted.
- [ ] Original data is present.
- [ ] Read/write test succeeds.
- [ ] `/etc/fstab` mount survives reboot.
- [ ] Old volume is deleted only after validation.

---

# Cleanup

To avoid charges:

1. Terminate temporary EC2 test instances.
2. Terminate the original EC2 instance when the lab is complete.
3. Delete unused EBS volumes.
4. Deregister source and copied AMIs.
5. Delete unused AMI backing snapshots.
6. Delete the manual EBS snapshot.
7. Remove unused security groups and key pairs.

---

# Interview Questions

1. What is an AMI?
2. Is an AMI global or Regional?
3. Can an EBS volume be attached across Availability Zones?
4. What is the difference between an AMI and an EBS snapshot?
5. Why must a filesystem be unmounted before detaching the volume?
6. Why is UUID preferred in `/etc/fstab`?
7. Why may `/dev/sdf` appear as `/dev/nvme1n1`?
8. Can an attached EBS volume be deleted?
9. What happens when an AMI is copied to another Region?
10. Why should the old EBS volume be retained until validation is complete?
