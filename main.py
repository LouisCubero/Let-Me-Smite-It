import nextcord
from nextcord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import heapq
from dataclasses import dataclass, field

# Guilty Until Proven Innocent Protocol

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# Note: All Discord bots require "intents".

intents = nextcord.Intents.default()
intents.members = True  # Note: Discord refers to "users" as "members".
intents.message_content = True

@dataclass

# Detects common keywords spammers like to use.
class spam_detector:
    spam_keywords: set[str] = field(default_factory=lambda:{
        "@everyone,", "@here", "crypto", "nitro", "us citizen", "tickets", "giveaway"
    })

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_users = {}  # Probationary period for new users, 60 min timer.
        self.new_users_heap = []  # Newest member on top of heap.

        # Anti-spam tools.
        self.SPAM_WEBHOOK = os.getenv("SPAM_WEBHOOK")
        self.spamDetector = spam_detector()

    # Stores data from "on_member_join" into "new_users" dictionary.
    def add_new_user(self, member):
        join_time = datetime.now(timezone.utc)  # Timestamp of recently joined user.
    
        self.new_users[member.id] = {
            "join_time": join_time,
            "message_count": 0,
            "is_spammer": False,
        }
        # Adds user to "new_users_heap".
        heapq.heappush(self.new_users_heap, (join_time, member.id))
        print(f"User {member.name} added to the heap at {join_time}")

    # User removed from probationary period after timer is done.
    def remove_old_users(self):
        now = datetime.now(timezone.utc)

        # join_time compared to 60 minutes after recorded timestamp.
        while self.new_users_heap and (now - self.new_users_heap[0][0]).total_seconds() > 40:
            join_time, user_id = heapq.heappop(self.new_users_heap)
            del self.new_users[user_id]
            print(f"Removed user {user_id} from probationary period!")

    # Checks user on top of heap every 5 minutes, user removed from "new_users" after 60 minutes.
    @tasks.loop(seconds=30)
    async def check_for_old_users(self):
        self.remove_old_users()

    # Appends user to "new_users" when they join server.
    async def on_member_join(self, member):
        self.add_new_user(member)

# Bot prefix is "!".
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

# Starts loop to check new_user condition every 5 minutes.
bot.check_for_old_users.start()

bot.run(DISCORD_TOKEN)