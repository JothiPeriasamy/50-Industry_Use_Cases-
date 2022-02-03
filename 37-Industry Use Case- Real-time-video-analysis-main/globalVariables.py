# Video Parameters
GLOBAL_ROW = 720
# Scale according to the size of the row
GLOBAL_COL = 720
GLOBAL_FPS = 30

# Spark Configuration
GLOBAL_BATCH_DURATION = 2
GLOBAL_WINDOW_DURATION = 10
GLOBAL_SLIDE_DURATION = 10
GLOBAL_BROKER = "localhost:9092"

# Live Video Address
#GLOBAL_STREAM_ADDRESS = 'https://www.youtube.com/watch?v=9uT9rJh9tZw'

GLOBAL_STREAM_ADDRESS = input("Enter the youtube url:")