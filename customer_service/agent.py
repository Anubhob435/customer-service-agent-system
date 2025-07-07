
"""Agent module for the customer service agent."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from .sub_agents.googlesearchagent import academic_websearch_agent
from .sub_agents.inventoryAgent import librarian_agent
from .sub_agents.Databaseagent import database_agent 
import logging
import warnings
from google.adk import Agent
from .config import Config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION
from .shared_libraries.callbacks import (
    rate_limit_callback,
    before_agent,
    before_tool,
    after_tool
)
from .tools.tools import (
    send_call_companion_link,
    approve_discount,
    sync_ask_for_approval,
    update_salesforce_crm,
    access_cart_information,
    modify_cart,
    get_book_recommendations,
    check_product_availability,
    schedule_reading_consultation,
    get_available_consultation_times,
    send_reading_recommendations,
    generate_qr_code,
)

from .sub_agents.googlesearchagent import academic_websearch_agent

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

configs = Config()

# configure logging __name__
logger = logging.getLogger(__name__)


root_agent = Agent(
    model=configs.agent_settings.model,
    global_instruction=GLOBAL_INSTRUCTION,
    instruction=INSTRUCTION,
    name=configs.agent_settings.name,
    tools=[
        send_call_companion_link,
        approve_discount,
        sync_ask_for_approval,
        update_salesforce_crm,
        access_cart_information,
        modify_cart,
        get_book_recommendations,
        check_product_availability,
        schedule_reading_consultation,
        get_available_consultation_times,
        send_reading_recommendations,
        generate_qr_code,
        AgentTool(agent=academic_websearch_agent) , # Add the web search agent as a tool
        AgentTool(agent=librarian_agent)  # Add the librarian agent as a tool
    ],
    before_tool_callback=before_tool,
    after_tool_callback=after_tool,
    before_agent_callback=before_agent,
    before_model_callback=rate_limit_callback,
    
)
