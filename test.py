from bot import detect_intent

tests = [
    'i found a bug',
    'im frustrated',
    'see you later',
    'something is broken',
    'nobody is helping me',
    'this is urgent',
]

for t in tests:
    print(f'{t!r:40} → {detect_intent(t)}')