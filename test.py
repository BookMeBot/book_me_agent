def handle_user_message(user_message_history):

    callLLM(
        prompt: "
          We have a message and message history from the user:
          BEGIN USER MESSAGE HISTORY
          $user_message_history
          END USER MESSAGE HISTORY

          We need to decide the best next action to take. Call the appropriate function out of:

          - ask_user_question -- get more info from the user
          ...
        ",
        functions: [
            {
                name: ask_user_question,
                description: ...,
                input_schema: {
                    type: object
                    fields: [
                        {
                            name: quesion
                            type: string
                            description: "the question to ask the user"
                        }
                    ]
                }
            },
            {
                name: "make_booking",
                description: "make a hotel booking on behalf of the user",
                input_schema: {
                    type: object,
                    fields: [
                        {
                            name: hotel_name,
                            amentities: ? optional
                            ...
                        }
                        {
                            name: max_price,
                            type: number
                            // descripton
                        }
                    ]
                }
            }
        ],
    )


    # result from LLM:

    # new_assistant_message:
    #   [
    #      text block
    #      text: "i've decided to make a booking"

    #      tool call block
    #      tool name: 
    #   ]

    #find a tool call and then call my python function based on tool call w info

    # only call function when I have all fields thats part of function calling 

    # if not automating conversation then no need for langchain
    