# Guilty Until Proven Innocent

A discord bot that punishes spammers, without AI!

# The Workflow
A. Spammer joins server:
-> automatically added to probationary period.
-> if their first message includes: links, emails, mentions cash, crypto, nitro, fake job hiring.
-> user gets kicked, message is logged for any false positives.

B. Discord user joins server:
-> automatically added to probationary period.
-> user sends a normal message like "hi", as their first message, they get removed from probationary period.
-> This means they can previously restricted vocabulary. (links, emails, etc.)

C. Non-talkative user joins server:
-> automatically added to probationary period.
-> user doesn't send a message for 60 minutes...
-> removed from probationary period, can use restricted vocabulary.

# How it works:
-> New server members are stored in a hashmap and sorted in a heap based on how recently they joined.

-> We temporarily store: Discord ID, Timestamp, and whether they sent a message or not.

-> After 60 minutes OR if they've sent a non-spammy message, they get removed from probationary period and can send unrestricted messages.

# We use:
-> Hashsets: Targetted toward obvious spammers, uses very little memory and space.
-> Regex: Covers the remainder of spammy messages that the hashsets can't cover.
-> Discord Webhook: Any user that gets kicked, will have their message logged- learning from any false positives.
-> Nextcord: Awesome wrapper for the discord api, makes things super easy.

# Future Prospects
1. Collect and showcase a public database of spammers, for research purpose.
2. Gain some community owner feedback, seeing what they want.
3. Make scalable code, attempting to cover some edge cases.

- This is still a work in progress, gonna gain feedback and make awesome features! -
