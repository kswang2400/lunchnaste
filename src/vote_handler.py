def get_vote_message():
    return {
        'text': 'Where should we eat?',
        'attachments': [
            {
                'text': 'Which building should we go for lunch?',
                'callback_id': 'foo', # KW: TODO we need something to accept this post
                'color': '#3AA3E3',
                'attachment_type': 'default',
                'actions': [
                    {
                        'name': '651',
                        'text': '651',
                        'type': 'button',
                        'value': '651'
                    },
                    {
                        'name': '505',
                        'text': '505',
                        'type': 'button',
                        'value': '505'
                    },
                ]
            }
        ]
    }