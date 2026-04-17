# Link Failure Detection and Recovery with POX and Mininet

## Project Overview

This project demonstrates **link failure detection and recovery** in a **Software-Defined Network (SDN)** using **POX** as the controller and **Mininet** to simulate the network. The system automatically detects link failures between switches and recovers traffic flow using **OpenFlow** match-action rules. The solution is implemented using POX's **discovery** module and **learning switch** to handle link failures dynamically.

## Setup and Execution Steps

### 1. **Install POX** and **Mininet**:

   - **POX**: Clone the POX repository from GitHub and install its dependencies.
     ```bash
     git clone https://github.com/noxrepo/pox.git
     ```

   - **Mininet**: Install Mininet by following the [official instructions](https://mininet.org/download/).

### 2. **Start POX**:

   Run the following command to start the POX controller with the **link failure recovery** script:
   ```bash
   python3 ~/pox/pox.py link_failure_recovery
   ```
3. Start Mininet:

In a separate terminal, start Mininet with POX as the remote controller:
```bash

sudo mn --controller=remote,ip=127.0.0.1,port=6633
```
4. Test Link Failure and Recovery:

Run the following commands in Mininet CLI to simulate a link failure and recovery:

Before Link Failure:
```bash
pingall
```

Simulate Link Failure:
```bash

link h1 s1 down
pingall
```

Recover the Link:
```bash

link h1 s1 up
pingall
```

Expected Outcome:

Before the failure: pingall shows 2/2 received.
During failure: pingall shows 0/2 received.
After recovery: pingall shows 2/2 received again.
Expected Output
Before the link failure: The network will work normally with 2/2 received packets for pingall.
During the link failure: Traffic will be blocked, resulting in 0/2 received packets.
After the link recovery: Traffic will be restored with 2/2 received packets.
Screenshots/Logs
Wireshark Logs:
Capture the traffic before, during, and after the link failure. Show the differences in the traffic flow.
POX Logs:
Show POX logs that indicate the detection of the link failure and the installation of recovery flow rules.
iperf Results (Optional):
Capture the network throughput before, during, and after the link failure using iperf.
Example Output:

Before Link Failure:
```bash

h1 -> h2: 2/2 packets received
```
During Link Failure:
```bash
h1 -> h2: 0/2 packets received
```
After Link Recovery:
```bash
h1 -> h2: 2/2 packets received
```
Code Explanation
link_failure_recovery.py:

This script uses POX to handle OpenFlow events and detect link failures using the Discovery module. When a link failure is detected, POX automatically installs flow rules to reroute traffic and recover connectivity.
```bash

from pox.core import core
from pox.lib.revent import *
from pox.openflow import *
from pox.openflow.discovery import Discovery
from pox.forwarding.l2_learning import LearningSwitch
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class LinkFailureRecovery(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        core.openflow_discovery.addListeners(self)

    def _handle_ConnectionUp(self, event):
        log.info("Switch %s has connected", event.dpid)
        LearningSwitch(event.connection, transparent=False)
        log.info("Learning switch set up for switch %s", event.dpid)

    def _handle_LinkEvent(self, event):
        if event.removed:
            link = event.link
            log.info("Link failure detected between %s:%s and %s:%s", 
                     link.dpid1, link.port1, link.dpid2, link.port2)
            self.recover_flow_rules(link.dpid1)

    def recover_flow_rules(self, dpid):
        log.info("Installing recovery flow rules for Switch %s", dpid)
        flow = of.ofp_flow_mod()
        flow.match = of.ofp_match(in_port=1)
        flow.actions.append(of.ofp_action_output(port=2))
        core.openflow.sendToDPID(dpid, flow)

def launch():
    if not core.hasComponent("openflow_discovery"):
        from pox.openflow.discovery import launch as dl
        dl()

    core.registerNew(LinkFailureRecovery)
```


<img width="2485" height="931" alt="image" src="https://github.com/user-attachments/assets/a1a98a5f-fcaa-4697-87fd-be9591035d36" />
<img width="1825" height="1128" alt="image" src="https://github.com/user-attachments/assets/4febb7ee-2202-435d-8d1b-366cbdc6807a" />
<img width="1688" height="723" alt="image" src="https://github.com/user-attachments/assets/137fc8b3-ec66-4c90-af8a-e9de036ecdb8" />



