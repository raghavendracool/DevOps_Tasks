# Part 4 — Replace the Non-Root EBS Volume

[← Part 3](README_PART3.md) | [Next →](README_PART5.md)

## 1. Back Up and Unmount
```bash
sudo lsof +f -- /data
sudo tar -czf /tmp/data-backup.tar.gz -C /data .
sudo umount /data
```
Remove or comment the old UUID in `/etc/fstab`.

## 2. Detach Old Volume
EC2 Console → Volumes → old data volume → **Detach volume**. Wait for `Available`. Do not delete it yet.

## 3. Create and Attach New Volume
Create an 8 GiB gp3 volume in the same AZ and attach as `/dev/sdg`.

```bash
lsblk -f
sudo mkfs.ext4 /dev/nvme1n1
sudo mkdir -p /data
sudo mount /dev/nvme1n1 /data
sudo tar -xzf /tmp/data-backup.tar.gz -C /data
```

## 4. Persist and Verify
```bash
sudo blkid /dev/nvme1n1
```
Add the new UUID to `/etc/fstab`, then:
```bash
sudo umount /data
sudo mount -a
findmnt /data
cat /data/verification.txt
sudo reboot
```
Reconnect and verify again. Only then delete the old EBS volume.

> Never run `mkfs` until you have positively identified the new empty device.
