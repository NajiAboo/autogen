import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": "gpt-3.5-turbo-1106"
    }
)

llm_config_writer = {
    "timeout": 300,
    "temperature": 1,
    "seed": 50,
    "config_list": config_list
}


writer_agent = autogen.AssistantAgent(
    name="writer",
    llm_config= llm_config_writer,
    system_message="Your task is to write an article about a given subject and to rewrite it based on the feedback from the editor. Reply with TERMINATE after you create a corrected version."
)


llm_config_editor = {
     "timeout": 300,
    "temperature": 0,
    "seed": 50,
    "config_list": config_list
}

editor_agent = autogen.AssistantAgent(
    name="editor",
    llm_config=llm_config_editor,
    system_message="Your task is to correct the article submitted by the writer. Check if informations are accurate. Do not rewrite the article, instead create a list of ajustment to be made"
)


user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="a human admin",
    human_input_mode="TERMINATE",
    is_termination_msg= lambda x: x.get("content","") and x.get("content","").rstrip().endswith("TERMINATE")
)


group_chat = autogen.GroupChat(
    agents=[user_proxy, writer_agent, editor_agent],
    messages=[],
    max_round=10,
    speaker_selection_method="auto"
)

manager = autogen.GroupChatManager(
    groupchat=group_chat, 
    llm_config = llm_config_editor
)

user_proxy.initiate_chat(
    manager, 
    message="Write an article about Large Lanage Models"
)

