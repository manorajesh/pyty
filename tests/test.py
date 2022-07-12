import textwrap
class colors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSED = '\033[7m'
    RESET = '\033[0m'

wordlist = ["the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog", "the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog", "the", "quick", "brown", "fox", "jumped", "over", "the", "lazy", "dog"]
text = textwrap.wrap(" ".join(wordlist), width=75)
print("\n".join(text))
print(colors.REVERSED + "yes" + colors.RESET)
message = (colors.REVERSED + "asdfasdfasdf" + colors.RESET)
print(message[4])