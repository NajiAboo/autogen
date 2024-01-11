import autogen

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-3.5-turbo"]
    }
)

llm_config = {
    "temperature": 0,
    "timeout": 300,
    "seed": 1,
    "config_list": config_list 

}

assistant = autogen.AssistantAgent(
    name ="Assistant",
    system_message="You are a helpful assistant",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    is_termination_msg= lambda x: x.get("content", "").rstrip().endswith("TERMINATE")
)


user_proxy.initiate_chat(assistant, message=" Calculate 4 * 3")