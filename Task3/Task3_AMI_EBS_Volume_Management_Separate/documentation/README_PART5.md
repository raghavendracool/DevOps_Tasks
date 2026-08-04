# Part 5 — Verification, Cleanup, Troubleshooting and Interview Q&A

[← Part 4](README_PART4.md) | [Main](../README.md)

## Verification
```bash
lsblk -f
df -hT
findmnt /data
cat /data/verification.txt
```
Confirm source AMI, destination AMI, destination EC2, and replacement EBS are working.

## Troubleshooting
- Volume missing: `lsblk`, `sudo nvme list`, and confirm same AZ.
- Detach blocked: check `sudo lsof +f -- /data` and unmount.
- Mount failure: check `sudo file -s <device>` and `lsblk -f`.
- Boot issue: correct `/etc/fstab`; use `nofail`; test with `sudo mount -a`.
- AMI copy failure: check AMI state, IAM/KMS permissions and snapshot status.

## Cleanup
Terminate test instances, deregister copied/source AMIs, delete unneeded snapshots and EBS volumes, then remove unused Security Groups. Deregistering an AMI does not automatically remove every snapshot.

## 15 Interview Questions
1. **What is an AMI?** A regional EC2 launch template backed by snapshots.
2. **Is an AMI global?** No; copy it between Regions.
3. **What is EBS?** Persistent block storage for EC2.
4. **Can EBS attach across AZs?** No.
5. **Does stopping EC2 delete EBS?** Normally no.
6. **Root vs data volume?** OS storage versus additional application storage.
7. **Why unmount first?** To flush writes and prevent corruption.
8. **Why UUID in fstab?** Stable identification despite device-name changes.
9. **Why `nofail`?** Prevent optional-volume failure from blocking boot.
10. **Does AMI creation create snapshots?** Yes for included EBS volumes.
11. **Can copied AMIs be encrypted?** Yes, with proper KMS permissions.
12. **What changes cross-region?** New AMI ID and snapshots; network/key resources must be recreated or selected.
13. **Safe replacement process?** Backup, unmount, detach, attach, restore, verify, then delete old.
14. **Can EBS size increase?** Yes; then extend partition/filesystem.
15. **Risk of `mkfs` on wrong disk?** Existing data may be destroyed.
