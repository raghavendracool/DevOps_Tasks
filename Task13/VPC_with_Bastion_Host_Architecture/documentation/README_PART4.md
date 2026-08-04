# Part 4 — Bastion SSH Access and Verification

[← Part 3](README_PART3.md) | [Next: Part 5 →](README_PART5.md)

## Recommended Method — ProxyJump

From your local machine:

```bash
chmod 400 task13-key.pem
```

Connect directly through the Bastion Host:

```bash
ssh \
  -i task13-key.pem \
  -J ubuntu@<BASTION_PUBLIC_IP> \
  ubuntu@<PRIVATE_EC2_IP>
```

This method keeps the private key on your local machine.

## SSH Config Method

Create:

```bash
nano ~/.ssh/config
```

Add:

```text
Host task13-bastion
    HostName <BASTION_PUBLIC_IP>
    User ubuntu
    IdentityFile ~/.ssh/task13-key.pem

Host task13-private
    HostName <PRIVATE_EC2_IP>
    User ubuntu
    IdentityFile ~/.ssh/task13-key.pem
    ProxyJump task13-bastion
```

Secure:

```bash
chmod 600 ~/.ssh/config
chmod 400 ~/.ssh/task13-key.pem
```

Connect:

```bash
ssh task13-private
```

## Alternative Training Method — Copy Key to Bastion

This is easy but less secure.

Copy the key:

```bash
scp -i task13-key.pem \
  task13-key.pem \
  ubuntu@<BASTION_PUBLIC_IP>:/home/ubuntu/
```

Connect to Bastion:

```bash
ssh -i task13-key.pem \
  ubuntu@<BASTION_PUBLIC_IP>
```

On Bastion:

```bash
chmod 400 task13-key.pem

ssh -i task13-key.pem \
  ubuntu@<PRIVATE_EC2_IP>
```

Delete the copied key after the lab:

```bash
shred -u task13-key.pem
```

## Agent Forwarding Method

Start agent locally:

```bash
eval "$(ssh-agent -s)"
ssh-add task13-key.pem
```

Connect with forwarding:

```bash
ssh -A -i task13-key.pem \
  ubuntu@<BASTION_PUBLIC_IP>
```

From Bastion:

```bash
ssh ubuntu@<PRIVATE_EC2_IP>
```

Use agent forwarding only when the Bastion Host is trusted and hardened.

## Verify Private Connectivity

On the private EC2:

```bash
hostname
hostname -I
ip route
```

Expected:

```text
Private IP from 10.0.2.0/24
No public IP assigned
```

## Verify Outbound Internet Through NAT

If NAT Gateway exists:

```bash
curl -I https://aws.amazon.com
sudo apt update
```

Check public egress IP:

```bash
curl -s https://checkip.amazonaws.com
```

It should show the NAT Gateway Elastic IP, not an EC2 public IP.

## Verify No Direct SSH

From your laptop, this should fail:

```bash
ssh -i task13-key.pem \
  ubuntu@<PRIVATE_EC2_IP>
```

The private IP is not internet-routable.

## Copy a File Through Bastion

Using ProxyJump:

```bash
scp \
  -i task13-key.pem \
  -o ProxyJump=ubuntu@<BASTION_PUBLIC_IP> \
  test.txt \
  ubuntu@<PRIVATE_EC2_IP>:/home/ubuntu/
```

## Verify Logs

On Bastion:

```bash
sudo journalctl -u ssh --since "30 minutes ago"
sudo tail -100 /var/log/auth.log
```

On private EC2:

```bash
sudo tail -100 /var/log/auth.log
```

## Verification Checklist

- [ ] Local SSH to Bastion succeeds
- [ ] Bastion to private EC2 succeeds
- [ ] ProxyJump succeeds
- [ ] Private EC2 has no public IP
- [ ] Direct internet SSH to private IP fails
- [ ] Private outbound internet works through NAT when configured
- [ ] Authentication logs reviewed
