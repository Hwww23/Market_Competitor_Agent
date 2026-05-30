from agent import clean_json

assert clean_json('```json\n{"name": "Spotify"}\n```') == '{"name": "Spotify"}'
assert clean_json('{"name": "Spotify"}') == '{"name": "Spotify"}'
assert clean_json('```\n{"name": "Spotify"}\n```') == '{"name": "Spotify"}'
assert clean_json('```JSON\n{"name": "Spotify"}\n```') == '{"name": "Spotify"}'