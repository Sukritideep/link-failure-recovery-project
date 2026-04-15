# link-failure-recovery-project

# Link Failure Detection and Recovery with POX and Mininet

## Project Overview

This project demonstrates **link failure detection and recovery** in a **Software-Defined Network (SDN)** using **POX** as the controller and **Mininet** to simulate the network. The system automatically detects link failures between switches and recovers traffic flow using **OpenFlow** match-action rules. The solution is implemented using POX's **discovery** module and **learning switch** to handle link failures dynamically.

## Setup and Execution Steps

### 1. **Install POX** and **Mininet**:
   Follow the steps below to set up **POX** and **Mininet** on your machine:
   - **POX**: Clone the POX repository and install dependencies.
   - **Mininet**: Install Mininet following the official documentation.
   
### 2. **Start POX**:
   - In your **POX directory**, run:
   ```bash
   python3 ~/pox/pox.py link_failure_recovery
