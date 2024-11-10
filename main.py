import nextcord
from nextcord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import heapq

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# All Discord bots require "intents".
intents = nextcord.Intents.default()
intents.members = True  # Discord refers to "users" as "members".
intents.message_content = True

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_users = {}  # New users added here for 60 minutes, removed when time expires.
        self.new_users_heap = []  # Newest member on top of heap.

        self.ping_spam_protection = {}
        self.link_spam_protection = {}
        self.monetary_spam_protection = {}

    # Stores data from "on_member_join" into "new_users" dictionary.
    def add_new_user(self, member):
        join_time = datetime.now(timezone.utc)  # Timestamp of user that recently joined.
    
        self.new_users[member.id] = {
            "join_time": join_time,
            "message_count": 0,  # Optionally track the number of messages
        }
        # Adds user to "new_users_heap".
        heapq.heappush(self.new_users_heap, (join_time, member.id))
        print(f"User {member.name} added to the heap at {join_time}")

    # Removes user after 60 minutes from safety mode.
    def remove_old_users(self):
        now = datetime.now(timezone.utc)
        # Compares join_time to 60 minutes after.
        while self.new_users_heap and (now - self.new_users_heap[0][0]).total_seconds() > 3600:
            join_time, user_id = heapq.heappop(self.new_users_heap)
            del self.new_users[user_id]
            print(f"Removed user {user_id} from safety mode!")

    # Checks user on top of heap every 30 seconds, then removes user if 60 minutes have passed.
    @tasks.loop(minutes=5)
    async def check_for_old_users(self):
        self.remove_old_users()

    # Appends user to "new_users" when they join server.
    async def on_member_join(self, member):
        self.add_new_user(member)

# Instantiate the custom Bot class
bot = Bot(command_prefix='!', case_insensitive=True, intents=intents)

@bot.command()
async def hello(ctx):
    await ctx.reply("What's cracking cuh?")

@bot.command()
async def check_users(ctx):
    """Check the current new users stored in the dictionary."""
    if bot.new_users:
        user_list = "\n".join([f"{user_id}: {user_info}" for user_id, user_info in bot.new_users.items()])
        await ctx.send(f"Current new users:\n{user_list}")
    else:
        await ctx.send("No new users added yet.")

# Start the loop to check for old users every 30 seconds
bot.check_for_old_users.start()

# Run the bot
bot.run(DISCORD_TOKEN)