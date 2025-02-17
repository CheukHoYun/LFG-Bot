from discord.ext import tasks
from lfg_request import RequestManager

rq_mgr = RequestManager()

# Report the current state of the bot in console every 60 seconds
@tasks.loop(seconds=60)
async def report_state(client):
    requests = "==========\n[State Report]\tReporting current request list:"
    for user, rq in rq_mgr.requests.items():
        user_obj = await client.fetch_user(user)
        requests += f"\t {user_obj.name}\t" + rq.__str__()
    print(requests)
    print("==========")
