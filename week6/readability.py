from cs50 import get_string
from regex import match


def get_text():
    """Get text from the user."""
    text = get_string("Text: ")
    return text


def counter_variables(text):
    """ Initialize some counter variables and eventually write them to a
    dict."""
    counters = {}
    letters = 0
    words = 1
    sentences = 0

    # Iterate over every letter of the text to see if it's a letter, a space, or
    # the end of a sentence, and increase the corresponding counter.
    for char in text:
        m = match(r'\w', char)
        punct = match(r'[.!?]', char)
        if m:
            letters += 1
        elif char == " ":
            words += 1
        elif punct:
            sentences += 1

    # Write the results of the counts to the dictionary and return it.
    counters["letters"] = letters
    counters["words"] = words
    counters["sentences"] = sentences

    return counters


def coleman_liau(counters):
    """Calculate Colmean-Liau index of user's text."""

    # Store the previously obtained counts to some variables.
    letters = counters["letters"]
    words = counters["words"]
    sentences = counters["sentences"]
    L = letters / words * 100
    S = sentences / words * 100

    # Get grade level rounded to the nearest integer
    grade = round(0.0588 * L - 0.296 * S - 15.8)
    return grade


def print_grade(grade):
    """Print reading level of the text."""

    if grade >= 16:
        print(f"Grade {grade}")
    elif grade < 1:
        print("Before Grade 1.")
    else:
        print(f"Grade {grade}")


def main():
    """Print the reading level of a given text based on the Coleman-Liau
    index."""

    text = get_text()
    counters = counter_variables(text)
    grade = coleman_liau(counters)
    print_grade(grade)
    return 0


main()
