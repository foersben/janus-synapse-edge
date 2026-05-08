# 🛠️ Preparation: The "Safe-Stack" Configuration

The summarized **"Hybrid-Resilience" Configuration**: While our main server operates on a "Crash-Safe" philosophy (No-UPS), the critical Data Layer is now fully protected by dedicated hardware. This setup maximizes data consistency and protects the longevity of our NVMe drives.

Before burning the first ISO, here are the three most important levers to adjust during installation:

#### 1. The "RAM Shock Absorber" (SurrealDB on Intel NUC)
Since our **Intel NUC10i5FNH** (acting as the "Edge-Tier Brain") is backed by the **Eaton 3S 550 DIN UPS**, we can prioritize SSD longevity and performance over standard database write-paranoia.
* **Action:** On the NUC’s ZFS dataset for SurrealDB, set the property to `sync=disabled` and increase the transaction group timeout (`zfs_txg_timeout=120`).
* **Effect:** SurrealDB executes thousands of micro-writes directly in the NUC’s 16GB DDR4 RAM. Every 2 minutes, ZFS packages this state and flushes it as a single, highly efficient contiguous block to the 250GB NVMe, reducing SSD wear-and-tear by 90%.
* **Connectivity:** The NUC and the main server communicate via the **NETGEAR GS308E Managed Switch**, ensuring isolated, high-speed database traffic.

#### 2. Restic/Rclone: The "Heartbeat" Backup
Since the main Proxmox host is expected to lose power instantly during an outage, our backup is our ultimate safety net.
* **Interval:** The Restic cronjob is set to run **every 3 hours** (incremental).
* **Encryption:** Utilizing PHE (partially homomorphic encryption), data is encrypted on the server before being uploaded to Dropbox.
* **Tip:** Use `restic --limit-upload` during the initial setup to prevent the backup from saturating our bandwidth while working.

#### 3. The "Cold-Start" Plan (Proxmox Installation)
When setting up the main server (14700K / 5070 Ti), follow this strict sequence:
1.  **BIOS Thermal Tuning:** Set PL1/PL2 to **180W** to manage heat within the Jonsbo Z20 chassis.
2.  **BIOS Power Policy:** Set "Restore on AC/Power Loss" strictly to **Power Off**. This ensures the server remains dormant until the grid stabilizes and the UPS-backed NUC sends a Wake-on-LAN packet.
3.  **Proxmox:** Use **ZFS Native Encryption** with a strong passphrase (required at every manual boot).
4.  **Talos OS:** Inject the **56GB Hugepages** reservation into your `talos-machineconfig.yaml` for VM 1 (Do NOT configure this on the Proxmox host to prevent memory locking errors).

---

### 📝 Setup Roadmap (Initial Steps)

The order in which to realise the concept:

1.  **Step 1: BIOS Tuning** (VT-d, IOMMU, Power Limits, and "Stay Off" rules).
2.  **Step 2: Proxmox Installation** (ZFS Encrypted on the 2TB FireCuda 530).
3.  **Step 3: The "Taming"** (ARC-Limit to 8GB and Swap removal).
4.  **Step 4: GPU Passthrough** (Assigning the RTX 5070 Ti to the "Tensor Worker" VM).

### A Note on Recovery:
Since we are operating without a UPS on the main host, the **Python Janitor Daemon** is critical. Upon reboot, it will query the UPS-backed NUC database to identify any tasks marked as `RUNNING` and forcefully delete the associated corrupted Docker sandboxes, allowing for a clean resume.

**Hint:** After any major configuration change or ingesting large amounts of data, manually trigger a backup with `restic backup /path/to/our/data`, this is our "manual airbag" during the transition phase.
