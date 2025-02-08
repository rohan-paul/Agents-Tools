"""
composio_slack.py

This module defines the composio_slack_tool function, which sets up and returns
the Slack integration tool provided by the Composio platform. This tool is used by
the slack_agent to send messages to a specified Slack channel.

Integrations in Composio are configuration objects that define how your application connects
to external services (like GitHub, Slack, or HubSpot). Each integration encapsulates authentication
credentials (OAuth Client ID/Secret), permission scopes, and API specifications that determine
how your users can interact with the external service.

The tool is created by initializing a ComposioToolSet and retrieving the Slack-specific
tools using the App.SLACK configuration.
"""

# Import the necessary classes from the composio_crewai package.
from composio_crewai import ComposioToolSet, App

def composio_slack_tool():
    """
    Initializes and returns the Slack integration tool.

    This function creates an instance of ComposioToolSet and retrieves the Slack tools
    by specifying App.SLACK. The returned tool is then used by the slack_agent to send
    messages to Slack.

    Returns:
        The Slack tool(s) obtained from the ComposioToolSet.
    """
    # Instantiate the ComposioToolSet.
    composio_toolset = ComposioToolSet()
    # Retrieve and return the Slack tools configured for the App.SLACK.
    return composio_toolset.get_tools(apps=[App.SLACK])
