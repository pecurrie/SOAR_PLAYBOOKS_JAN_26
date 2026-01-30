"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'ask_question_channel_1' block
    ask_question_channel_1(container=container)

    return

@phantom.playbook_block()
def ask_question_channel_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("ask_question_channel_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "question": "Hi tell me yes or no",
        "responses": "yes,no",
        "destination": "C0ACCHS1R7S",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("ask question channel", parameters=parameters, name="ask_question_channel_1", assets=["test123"], callback=get_response_1)

    return


@phantom.playbook_block()
def loop_get_response_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("loop_get_response_1() called")

    loop_state = phantom.LoopState(state=loop_state_json)

    if loop_state.should_continue(container=container, results=results): # should_continue evaluates iteration/timeout/conditions
        loop_state.increment() # increments iteration count
        get_response_1(container=container, loop_state_json=loop_state.to_json())
    else:
        send_message_1(container=container)

    return


@phantom.playbook_block()
def get_response_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("get_response_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    ask_question_channel_1_result_data = phantom.collect2(container=container, datapath=["ask_question_channel_1:action_result.data.*.qid","ask_question_channel_1:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'get_response_1' call
    for ask_question_channel_1_result_item in ask_question_channel_1_result_data:
        if ask_question_channel_1_result_item[0] is not None:
            parameters.append({
                "question_id": ask_question_channel_1_result_item[0],
                "context": {'artifact_id': ask_question_channel_1_result_item[1]},
            })

    if not loop_state_json:
        # Loop state is empty. We are creating a new one from the inputs
        loop_state_json = {
            # Looping configs
            "current_iteration": 1,
            "max_iterations": 3,
            "conditions": [
                ["get_response_1:action_result.summary.response_received", "==", "True"]
            ],
            "max_ttl": 60,
            "delay_time": 5,
        }

    # Load state from the JSON passed to it
    loop_state = phantom.LoopState(state=loop_state_json)

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get response", parameters=parameters, name="get_response_1", assets=["test123"], callback=loop_get_response_1, loop_state=loop_state.to_json())

    return


@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_1() called")

    get_response_1_result_data = phantom.collect2(container=container, datapath=["get_response_1:action_result.data","get_response_1:action_result.summary.response_received","get_response_1:action_result.parameter.context.artifact_id"], action_results=results)

    get_response_1_result_item_0 = [item[0] for item in get_response_1_result_data]
    get_response_1_summary_response_received = [item[1] for item in get_response_1_result_data]

    parameters = []

    parameters.append({
        "input_1": get_response_1_result_item_0,
        "input_2": get_response_1_summary_response_received,
        "input_3": None,
        "input_4": None,
        "input_5": None,
        "input_6": None,
        "input_7": None,
        "input_8": None,
        "input_9": None,
        "input_10": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1")

    return


@phantom.playbook_block()
def send_message_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("send_message_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    message_formatted_string = phantom.format(
        container=container,
        template="""Message received: {0}\n""",
        parameters=[
            "get_response_1:action_result.data.*.payloads.*.actions.*.name"
        ])

    get_response_1_result_data = phantom.collect2(container=container, datapath=["get_response_1:action_result.summary.response","get_response_1:action_result.data.*.payloads.*.actions.*.name","get_response_1:action_result.data.*.payloads.*.original_message.ts","get_response_1:action_result.parameter.context.artifact_id"], action_results=results)

    parameters = []

    # build parameters list for 'send_message_1' call
    for get_response_1_result_item in get_response_1_result_data:
        parameters.append({
            "blocks": get_response_1_result_item[0],
            "message": message_formatted_string,
            "destination": "C0ACCHS1R7S",
            "parent_message_ts": get_response_1_result_item[2],
            "context": {'artifact_id': get_response_1_result_item[3]},
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("send message", parameters=parameters, name="send_message_1", assets=["test123"], callback=debug_1)

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return