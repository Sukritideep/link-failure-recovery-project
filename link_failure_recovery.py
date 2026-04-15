from pox.core import core
from pox.lib.revent import *
from pox.openflow import *
from pox.openflow.discovery import Discovery
from pox.forwarding.l2_learning import LearningSwitch
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class LinkFailureRecovery(EventMixin):
    def __init__(self):
        # Listen to OpenFlow events (like ConnectionUp)
        self.listenTo(core.openflow)

        # Listen to the discovery component to catch LinkEvents
        # This ensures _handle_LinkEvent is triggered when link events happen
        core.openflow_discovery.addListeners(self)

    def _handle_ConnectionUp(self, event):
        """
        Triggered when a switch connects to the controller.
        """
        log.info("Switch %s has connected", event.dpid)

        # Instantiating the LearningSwitch correctly with connection
        LearningSwitch(event.connection, transparent=False)
        
        log.info("Learning switch set up for switch %s", event.dpid)

    def _handle_LinkEvent(self, event):
        """
        Triggered by the discovery module when a link is added or removed.
        """
        if event.removed:
            link = event.link
            log.info("Link failure detected between %s:%s and %s:%s", 
                     link.dpid1, link.port1, link.dpid2, link.port2)
            
            # Call recovery logic when a link is removed
            self.recover_flow_rules(link.dpid1)

    def recover_flow_rules(self, dpid):
        """
        Example logic to install a backup flow rule when a link fails.
        """
        log.info("Installing recovery flow rules for Switch %s", dpid)
        flow = of.ofp_flow_mod()
        flow.match = of.ofp_match(in_port=1)  # Match traffic coming from port 1
        flow.actions.append(of.ofp_action_output(port=2))  # Redirect to port 2
        
        # Send flow rule to the switch that experienced the failure
        core.openflow.sendToDPID(dpid, flow)

def launch():
    # Ensure the discovery module is running so LinkEvents work
    if not core.hasComponent("openflow_discovery"):
        from pox.openflow.discovery import launch as dl
        dl()
        
    # Register the LinkFailureRecovery component
    core.registerNew(LinkFailureRecovery)
