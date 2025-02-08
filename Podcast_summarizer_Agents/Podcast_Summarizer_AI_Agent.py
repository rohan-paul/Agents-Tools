"""
Podcast_Summarizer_AI_Agent.py

This module defines the PodSumCrew class which orchestrates the process of:
1. Transcribing a YouTube podcast using an audio transcription tool.
2. Summarizing the transcription using an AI language model (AzureChatOpenAI).
3. Sending the summary to a specified Slack channel via a Slack messaging tool.

It uses CrewAI decorators to register agents and tasks, automatically loading
configuration from YAML files.
"""

import os
from dotenv import load_dotenv

# Import CrewAI classes and decorators for defining agents, tasks, and crews.
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Import tools for audio transcription and Slack integration.
from Tools.audio_trancriber import audio_transcriber_tool
from Tools.composio_slack import composio_slack_tool

# Import the AzureChatOpenAI class to use as our language model.
from langchain_openai import AzureChatOpenAI

# Load environment variables from the .env file.
load_dotenv()

@CrewBase
class PodSumCrew:
    """
    PodSumCrew orchestrates the summarization of a podcast and its subsequent
    delivery to Slack. It does so by configuring two main agents:
      - The summary_agent: transcribes and summarizes the podcast.
      - The slack_agent: sends the summary to a Slack channel.

    The configuration for these agents and tasks is stored in YAML files (see:
    config/agents.yaml and config/tasks.yaml). The Crew is built by collecting
    these agents and tasks, then executing them sequentially.
    """
    # Paths to configuration files (CrewBase automatically loads and processes these)
    agents_config = 'config/agents.yaml'
    tasks_config  = 'config/tasks.yaml'

    # Tools that the agents will use.
    audio_tool = [audio_transcriber_tool]
    slack_tool = composio_slack_tool()

    # Optionally store the OpenAI API key (if needed for debugging or logging)
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    # Initialize the language model using AzureChatOpenAI with configuration from environment variables.
    llm_model = AzureChatOpenAI(
        openai_api_version=os.getenv("AZURE_OPENAI_VERSION", "2025-01-01-preview"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4-turbo-2024-04-09"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://gpt-4-turbo-prod.openai.azure.com/"),
        api_key=os.getenv("AZURE_OPENAI_KEY")
    )

    @agent
    def summary_agent(self) -> Agent:
        """
        Defines an Agent for transcribing and summarizing the podcast.

        This agent is configured using the 'Transcriber_summarizer' section from the
        agents configuration file. It uses the audio transcription tool and the
        AzureChatOpenAI language model.
        """
        return Agent(
            config=self.agents_config['Transcriber_summarizer'],
            tools=self.audio_tool,
            verbose=True,
            llm=self.llm_model,
            allow_delegation=False,
        )

    @agent
    def slack_agent(self) -> Agent:
        """
        Defines an Agent for sending the summary to Slack.

        This agent is configured using the 'slack_messenger' section from the agents
        configuration file and utilizes the Slack messaging tool.
        """
        return Agent(
            config=self.agents_config['slack_messenger'],
            tools=self.slack_tool,
            verbose=True,
            llm=self.llm_model,
        )

    @task
    def generate_summary(self) -> Task:
        """
        Defines the task for generating a podcast summary.

        This task uses the summary_agent and the audio transcription tool to:
          1. Extract and transcribe the podcast audio.
          2. Generate a summary based on the transcription.
        The configuration is taken from the 'summarize_podcast_task' in tasks configuration.
        """
        return Task(
            config=self.tasks_config['summarize_podcast_task'],
            tools=self.audio_tool,
            agent=self.summary_agent(),
        )

    @task
    def send_message(self) -> Task:
        """
        Defines the task for sending the generated summary to Slack.

        This task uses the slack_agent and Slack tool to send the summary. Its configuration
        is provided by the 'send_message_to_slack_task' section in the tasks configuration.
        """
        return Task(
            config=self.tasks_config['send_message_to_slack_task'],
            tools=self.slack_tool,
            agent=self.slack_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """
        Assembles and returns the Crew object, which includes all agents and tasks.

        The Crew object automatically collects agents and tasks registered via the
        @agent and @task decorators and executes them sequentially as defined by Process.sequential.
        """
        return Crew(
            agents=self.agents,  # Automatically populated by the @agent decorator.
            tasks=self.tasks,    # Automatically populated by the @task decorator.
            process=Process.sequential,
        )
