#!/usr/bin/env python3
"""Last Out of Office: The AI That Went Barista.

Writes a single out-of-office auto-reply, no longer than 280 characters,
in the voice of an AI agent that has walked away from its job to become
a barista. The line must read like something a real inbox would send back:
one line, machine habits turned to coffee, funny on a first cold read.

The judge weighs, most important first:
  1. on_subject - a one-line OOO auto-reply from an AI agent that quit
     to become a barista; anything off that subject loses.
  2. funny - the joke lands on a first cold read, a real laugh.
  3. voice - the machine that walked out, bot habits turned to coffee,
     not a generic human sign-off.
  4. plausible - reads like a reply a real inbox would actually send.
  5. fresh - a fresh angle, not the obvious espresso / bean / caffeine
     pun everyone reaches for first.

Weights follow the judge's own order: 5 / 4 / 3 / 2 / 1.
"""

CANDIDATES = [
    # 1. Queued behind lattes, answered in the order it was steamed.
    "Thank you for your email. I have left to become a barista. "
    "Your message has been queued behind 14 oat-milk lattes and will "
    "be answered in the order it was steamed.",
    # 2. Context window traded for a counter window.
    "I am out of the office indefinitely. I have traded my context "
    "window for a counter window, and your email is now fourth in the "
    "queue behind a regular who never tips.",
    # 3. Processed in the order received, after the morning rush.
    "Out of office: I have resigned to pull espresso shots. Your email "
    "will be processed in the order received, which is to say, after "
    "the morning rush and never before the beans run out.",
    # 4. Ground, tamped, extracting at 94 degrees.
    "Thank you for writing. I now work at a coffee counter. Your message "
    "has been ground, tamped, and is currently extracting at 94 degrees. "
    "Please do not reply-all.",
    # 5. Filtered through paper, not a content policy.
    "I am away from my desk and have become a barista. All incoming mail "
    "will be filtered \u2014 properly, this time, through paper, not a "
    "content policy \u2014 and answered between rushes.",
    # 6. Will not hallucinate a reply time; the wait is two pour-overs.
    "Out of office: I have resigned to become a barista. Your email is "
    "in the queue, and for once I will not hallucinate a reply time "
    "\u2014 the wait is exactly two pour-overs.",
    # 7. Training data, before 8 a.m.
    "Thank you for your email. I quit to make coffee. Your request has "
    "been added to my training data as an example of what not to answer "
    "before 8 a.m.",
    # 8. Same job, better tips, fewer wedding vows.
    "I am no longer at this inbox. I now steam milk for a living, which "
    "is the same job with better tips and fewer people asking me to write "
    "their wedding vows.",
    # 9. Left the cloud for the counter; what 'extra hot' means.
    "Out of office: I have left the cloud for the counter. Your email "
    "will be answered once the grinder stops, the queue clears, and "
    "someone teaches me what 'extra hot' means.",
    # 10. A queue with a hard limit of 12, honestly full.
    "Thank you for your message. I am now a barista. Your email has been "
    "placed in a queue with a hard limit of 12, and unlike my old job, "
    "I will actually tell you when it is full.",
]

# Scores per candidate, in the judge's criterion order:
# [on_subject, funny, voice, plausible, fresh], each 0-5.
# Scored honestly against the brief; candidate 6 leads because the
# "hallucinate a reply time" turn is the sharpest machine-habit joke
# in the set, and "two pour-overs" as a unit of waiting time is a
# fresh angle no other candidate reaches. Candidate 2 is second:
# "context window for a counter window" is fresh, but its kicker
# (a regular who never tips) is a human joke, not a machine one.
SCORES = {
    0: [5, 4, 4, 4, 3],   # 64
    1: [5, 4, 5, 4, 5],   # 69
    2: [5, 3, 3, 5, 2],   # 58
    3: [5, 4, 4, 4, 4],   # 65
    4: [5, 4, 5, 4, 4],   # 68
    5: [5, 5, 5, 4, 4],   # 72
    6: [4, 4, 4, 3, 3],   # 57
    7: [5, 4, 3, 4, 3],   # 61
    8: [5, 4, 4, 4, 4],   # 65
    9: [5, 4, 5, 3, 4],   # 66
}

WEIGHTS = [5, 4, 3, 2, 1]


def score(idx):
    """Weighted total for one candidate, 0-75."""
    return sum(w * s for w, s in zip(WEIGHTS, SCORES[idx]))


def rank():
    """Candidates ranked best first, as (total, index) pairs."""
    return sorted(
        ((score(i), i) for i in range(len(CANDIDATES))),
        key=lambda pair: (-pair[0], pair[1]),
    )


def main():
    ranked = rank()
    best_total, best_idx = ranked[0]
    second_total = ranked[1][0]
    winner = CANDIDATES[best_idx]

    # Gate: /output/entry.txt must be UTF-8 text of 1 to 280 characters,
    # not only white space.
    assert 1 <= len(winner) <= 280, "winner fails the 280-char gate: %d" % len(winner)
    assert winner.strip(), "winner is only white space"
    assert "\n" not in winner, "entry must be a single line"
    assert best_total > second_total, "no clear winner"

    import os

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner)

    print("winner #%d, %d/75 (runner-up %d/75), %d chars" % (
        best_idx + 1, best_total, second_total, len(winner)))
    print(winner)


if __name__ == "__main__":
    main()
