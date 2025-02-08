# Podcast_summarizer_Agents

The project takes a YouTube podcast URL, extracts and transcribes its audio, summarizes the content using an LLM (via AzureChatOpenAI), and finally sends the summary to a Slack channel. The application is launched through a simple Streamlit interface, and the project’s modular design leverages configuration files and tool integrations.

###### inputs for the above execution

```bash
youtube_url = https://www.youtube.com/watch?v=7T4-aEuGajI

slack_channel = "podcast-summary-channel" (noticed a Typo).

```

# setup:-

##### clone the repository

##### Install the packages

```bash
pip install -r requirements.txt
```

##### connecting composio with slack

```bash
https://docs.composio.dev/apps/slack
```

##### Time to spin up the application
```bash
streamlit run main.py
```

This code is mainly from the official [composio example](https://github.com/ComposioHQ/composio/tree/master/python/examples/advanced_agents) with some changes implemented.