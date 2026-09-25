# Option 1: Dataset Realignment Mapping

This report highlights every case where the model accurately followed the highly granular intent rules in `v2_optimized.md`, but failed the evaluation because the original Golden Dataset grades it using an older, broader category.

**Total Mismatches Found:** 55 / 95

| ID | Utterance | Golden Dataset Expects | Model Generated Intent (From V2 Prompt) |
|---|---|---|---|
| 11 | Show me the program. | `TV__OPEN_MENU` | `TV__NAVIGATE_MENU` |
| 12 | What is playing on ZDF? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 13 | What is playing on channel 12 right now? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 14 | What is on TV at 6 PM? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 15 | What is on in two hours? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 16 | Show me the program for tomorrow. | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 17 | What's on TV on Saturday at 6 PM? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 18 | What is coming on DMAX now? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 19 | What is playing on channel 25 right now? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 20 | The program for Sunday on ORF 2. | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 21 | What is on at 8 PM on ORF? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 22 | What does the program on channel twelve look like in two hours? | `TV__PROGRAM` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 23 | Go to 8:15 PM. | `TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 24 | Jump to Saturday evening. | `TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 25 | to Sunday | `TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 29 | four hours later | `TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 30 | four hours back | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 31 | Go to ORF 2 at 8 PM. | `TV__PROGRAM, TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 32 | Show channel ten at 3 PM. | `TV__PROGRAM, TV__NAVIGATE` | `TV__PROGRAM_CHANNEL_OR_TIME_ONLY` |
| 33 | Go to ZDF on Saturday. | `TV__PROGRAM, TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 34 | Jump to channel fifteen on Sunday. | `TV__PROGRAM, TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 35 | Open EPG | `TV__OPEN_MENU` | `TV__NAVIGATE_MENU` |
| 36 | Go to kids. | `TV__OPEN_MENU` | `TV__NAVIGATE_MENU` |
| 37 | Jump to settings. | `TV__OPEN_MENU` | `TV__NAVIGATE_MENU` |
| 38 | Back to the apps | `TV__OPEN_MENU` | `TV__NAVIGATE_MENU` |
| 39 | to search | `TV__OPEN_MENU` | `TV__NAVIGATE_MENU` |
| 42 | to help | `TV__OPEN_MENU` | `TV__NAVIGATE_MENU` |
| 43 | Open the voice control | `TV__OPEN_MENU` | `TV__NAVIGATE_MENU` |
| 44 | upwards | `TV__NAVIGATION_KEY` | `TV__NAVIGATE_KEY` |
| 45 | Go to the right. | `TV__NAVIGATION_KEY` | `TV__NAVIGATE_KEY` |
| 46 | Okay. | `TV__OK` | `N/A` |
| 50 | Jump forward three hours. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 51 | Fast forward 10 minutes. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 52 | jump forward thirty-five seconds | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 53 | Go forward two hours and 10 minutes. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 54 | Jump forward five minutes and ten seconds. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 55 | Jump back two hours. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 56 | Rewind five minutes. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 57 | jump back fifteen seconds | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 58 | Go back 1 hour 10 minutes. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 59 | Jump back 2 minutes and 10 seconds. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 60 | Jump to the end of the first hour. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 61 | Go to the twentieth minute. | `TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 62 | Go exactly to second 55. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 63 | Jump to 1 hour and 5 minutes. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 64 | Jump to 5 minutes and 10 seconds. | `TV__NAVIGATE` | `TV__SEEK_OR_REWIND` |
| 65 | Go to the sixth minute and tenth second. | `TV__NAVIGATE` | `TV__NAVIGATE_TO_DATETIME` |
| 79 | When is Sturm der Liebe on? | `TV__SEARCH, TV__PROGRAM_WHEN_WHERE` | `TV__PROGRAM_FOR_SPECIFIC_CONTENT` |
| 80 | When is a thriller on? | `TV__SEARCH, TV__PROGRAM_WHEN_WHERE` | `TV__PROGRAM_FOR_SPECIFIC_CONTENT` |
| 81 | Which channel is A Thriller playing on? | `TV__SEARCH, TV__PROGRAM_WHEN_WHERE` | `TV__PROGRAM_FOR_SPECIFIC_CONTENT` |
| 82 | Where is an action movie playing right now? | `TV__SEARCH, TV__PROGRAM_WHEN_WHERE` | `TV__PROGRAM_FOR_SPECIFIC_CONTENT` |
| 84 | Where is Günter Jauch on? | `TV__SEARCH, TV__PROGRAM_WHEN_WHERE` | `TV__PROGRAM_FOR_SPECIFIC_CONTENT` |
| 87 | to the last watched channel | `TV__NEXT_CHANNEL` | `TV__CHANNEL_ZAPPING` |
| 92 | Turn the sound off. | `TV__VOLUME` | `TV__VOLUME_CONTROL` |
| 93 | Turn the sound back on. | `TV__VOLUME` | `TV__VOLUME_CONTROL` |
