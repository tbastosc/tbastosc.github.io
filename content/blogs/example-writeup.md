---
title: "Setting Up a Home Lab for Security Testing"
date: 2025-01-02
draft: false
tags: ["Home Lab", "Security", "Virtualization", "Learning"]
image: images/post-homelab.png
---

A home lab is one of the best investments you can make in your cybersecurity career. It gives you a safe environment to practice offensive techniques, test defensive tools, and break things without consequences.

## What You Need

You don't need expensive hardware to get started. A decent laptop or desktop with at least 16GB of RAM and an SSD will handle most setups.

### Virtualization Platform

Pick one and learn it well:

- **Proxmox** (free, type-1 hypervisor) - great if you have a dedicated machine
- **VirtualBox** (free, type-2) - runs on any OS, good for beginners
- **VMware Workstation** (paid, type-2) - industry standard, free for personal use

### Essential VMs

Start with these virtual machines:

| VM | Purpose |
|---|---|
| Kali Linux | Offensive security toolkit |
| Ubuntu Server | Target for network/web attacks |
| Windows 10/11 | Active Directory lab target |
| Metasploitable | Intentionally vulnerable practice target |
| DVWA | Web application security testing |

## Network Architecture

Set up an isolated virtual network so your lab traffic doesn't leak onto your home network:

1. Create a **host-only** or **internal** network in your hypervisor
2. Give your Kali VM two NICs: one NAT (for internet) and one internal (for lab)
3. Put all target VMs on the internal network only
4. Use pfSense or OPNsense as a virtual firewall between segments

## Practice Resources

Once your lab is running, work through these:

- [HackTheBox](https://www.hackthebox.com) - online penetration testing labs
- [TryHackMe](https://tryhackme.com) - guided learning paths
- [OverTheWire](https://overthewire.org) - classic wargames
- [SANS Holiday Hack](https://www.sans.org/mlp/holiday-hack-challenge/) - annual CTF challenge

## Tips

- **Snapshot everything** before you break it. Snapshots are your undo button.
- **Document as you go.** Write down every command, every finding. This becomes your portfolio content.
- **Start small.** One Kali VM and one Metasploitable instance is enough to learn the fundamentals.
- **Automate your setup.** Once you find a configuration that works, script it with Vagrant, Ansible, or Terraform so you can rebuild in minutes.

---

*This is an example blog post. Replace it with your own content!*
