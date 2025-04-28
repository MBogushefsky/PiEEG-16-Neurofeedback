from pylsl import resolve_streams, StreamInlet

streams = resolve_streams()
inlet = StreamInlet(streams[0])
while True:
    sample, timestamp = inlet.pull_sample()
    print(f"Received: {sample} at {timestamp}")
