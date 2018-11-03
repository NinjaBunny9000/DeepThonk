import random

posits = (
			"tossed something with your fists",
			"held an 8-dick capacitor in your hands",
			"aggressively does the macarena",
			"pants'd loudly",
            "murdered ynneL in a waterin' hole?"
            )


def content():
    return posits[random.randrange(0, len(posits))]


def have_you_tho():
    msg = 'Have you ever ' + content() + '?'
    return msg

if __name__ == "__main__":
	print(have_you_tho())