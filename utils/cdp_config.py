# CDP AgentKit wrapper setup goes here
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper


def setup_cdp_toolkit():
    cdp = CdpAgentkitWrapper()
    return CdpToolkit.from_cdp_agentkit_wrapper(cdp)
