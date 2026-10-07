"""Compress verbose law school notes into compact outline form."""

import argparse
import re

# ---------------------------------------------------------------------------
# Phrase tables. Keys are lowercase; matching is case-insensitive,
# whole-phrase (so "Indiana" never mangles "Indianapolis"), and
# longest-match-first (so "West Virginia" wins over "Virginia").
#
# _FIXED: replacement used verbatim (acronyms, symbols, digits).
# _CASED: replacement's first letter follows the match, so one entry covers
#         both cases ("because" -> "bc", "Because" -> "Bc").
# _DELETIONS: phrases removed entirely.
# Add your own abbreviations to the relevant list; nothing else to change.
# ---------------------------------------------------------------------------

_FIXED = [
    # Legal terms
    ("personal jurisdiction", "PJ"),
    ("subject matter jurisdiction", "SMJ"),
    ("summary judgment", "SJ"),
    ("supreme court", "SCOTUS"),
    ("section", "§"),
    ("due process", "DP"),
    ("default judgment", "DJ"),
    ("articles of confederation", "AoC"),
    ("adverse possession", "AP"),
    ("intellectual property", "IP"),
    ("united states", "US"),
    # States
    ("alabama", "AL"), ("alaska", "AK"), ("arizona", "AZ"), ("arkansas", "AR"),
    ("california", "CA"), ("colorado", "CO"), ("connecticut", "CT"), ("delaware", "DE"),
    ("florida", "FL"), ("georgia", "GA"), ("hawaii", "HI"), ("idaho", "ID"),
    ("illinois", "IL"), ("indiana", "IN"), ("iowa", "IA"), ("kansas", "KS"),
    ("kentucky", "KY"), ("louisiana", "LA"), ("maine", "ME"), ("maryland", "MD"),
    ("massachusetts", "MA"), ("michigan", "MI"), ("minnesota", "MN"), ("mississippi", "MS"),
    ("missouri", "MO"), ("montana", "MT"), ("nebraska", "NE"), ("nevada", "NV"),
    ("new hampshire", "NH"), ("new jersey", "NJ"), ("new mexico", "NM"), ("new york", "NY"),
    ("north carolina", "NC"), ("north dakota", "ND"), ("ohio", "OH"), ("oklahoma", "OK"),
    ("oregon", "OR"), ("pennsylvania", "PA"), ("rhode island", "RI"), ("south carolina", "SC"),
    ("south dakota", "SD"), ("tennessee", "TN"), ("texas", "TX"), ("utah", "UT"),
    ("vermont", "VT"), ("virginia", "VA"), ("washington", "WA"), ("west virginia", "WV"),
    ("wisconsin", "WI"), ("wyoming", "WY"),
    # Connectors and symbols
    ("and", "+"),
    ("more than", ">"),
    ("less than", "<"),
    ("number", "#"),
    ("percentage", "%"),
    ("percent", "%"),
]

_CASED = [
    # Parties
    ("plaintiffs'", "p's"), ("plaintiff's", "p's"), ("plaintiffs", "p's"), ("plaintiff", "p"),
    ("defendants'", "d's"), ("defendant's", "d's"), ("defendants", "d's"), ("defendant", "d"),
    ("landlords'", "ll's"), ("landlord's", "ll's"), ("landlords", "ll's"), ("landlord", "ll"),
    ("tenants'", "t's"), ("tenant's", "t's"), ("tenants", "t's"), ("tenant", "t"),
    ("hypothetical", "hypo"),
    ("jurisdictions", "jdx's"), ("jurisdiction", "jdx"),
    ("corporation", "corp"),
    ("constitutional", "const"), ("constitution", "const"),
    ("administration", "admin"), ("administrative", "admin"),
    ("president", "pres"),
    ("secretary", "sec"),
    ("executive", "exec"),
    ("legislative", "legis"), ("legislature", "legis"),
    ("judicial", "judic"),
    ("contract", "k"),
    ("federal", "fed"),
    ("citizenship", "c-ship"),
    ("argument", "arg"),
    # Common words
    ("information", "info"),
    ("without", "w/o"), ("with", "w/"),
    ("professor", "prof"),
    ("government", "govt"),
    ("introduction", "intro"),
    ("people", "ppl"),
    ("automatically", "auto"),
    ("conversation", "convo"),
    ("combination", "combo"),
    ("technology", "tech"),
    ("apartment", "apt"),
    ("graduate", "grad"),
    ("regarding", "re."),
    ("especially", "esp."),
    ("professional", "prof."),
    ("education", "edu"),
    ("universities", "uni's"), ("university", "uni"),
    ("legitimate", "legit"),
    ("because", "bc"),
]

_DELETIONS = [
    "the", "an",
    "it", "it's",
    "is", "are", "was", "were",
    "his", "hers", "their", "theirs",
    "case example:",
]

# Lowercase-only deletions ("A" is kept so grades and labels survive).
_EXACT_DELETIONS = ["a"]

# Punctuation-free symbols: match anywhere (no word boundaries).
_RAW = (("->", "→"), ("<-", "←"))
# Thousands groupings: must follow a digit, must not be followed by one.
_NUM = ((",000,000,000", "B"), (",000,000", "M"), (",000", "K"))

# Generated groups ----------------------------------------------------------
_SUFFIXES = {1: "1st", 2: "2nd", 3: "3rd"}


def _ordinal(n):
    return _SUFFIXES.get(n, f"{n}th")


for _i, _word in enumerate(
    ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"), 1
):
    _FIXED.append((_word, str(_i)))

for _i, _word in enumerate(
    ("first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"), 1
):
    _FIXED.append((_word, _ordinal(_i)))

for _n, _word in enumerate(
    ("first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
     "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
     "seventeenth", "eighteenth", "nineteenth"), 1
):
    _code = f"{_n}A"
    _FIXED.append((f"{_ordinal(_n)} amendment", _code))
    _FIXED.append((f"{_word} amendment", _code))

for _modal in ("would", "should", "could", "might"):
    _CASED.append((_modal + " have", _modal + "'ve"))
for _full, _short in (
    ("does", "doesn't"), ("do", "don't"), ("will", "won't"),
    ("could", "couldn't"), ("would", "wouldn't"), ("should", "shouldn't"),
    ("have", "haven't"), ("can", "can't"), ("did", "didn't"),
    ("cannot", "can't"),
):
    _CASED.append((_full + " not", _short))

del _i, _word, _n, _code, _modal, _full, _short

# Single compiled pattern, longest phrase first ------------------------------
_entries = {}
for _phrase, _repl in _FIXED:
    _entries[_phrase] = (_repl, False)
for _phrase, _repl in _CASED:
    _entries[_phrase] = (_repl, True)
for _phrase in _DELETIONS:
    _entries[_phrase] = ("", False)
for _phrase, _repl in _RAW + _NUM:
    _entries[_phrase] = (_repl, False)

_word_keys = [p for p in _entries if p not in dict(_RAW + _NUM)]
_parts = [(len(p), r"(?<!\w)" + re.escape(p) + r"(?!\w)") for p in _word_keys]
_parts += [(len(p), re.escape(p)) for p, _ in _RAW]
_parts += [(len(p), r"(?<=\d)" + re.escape(p) + r"(?!\d)") for p, _ in _NUM]
_parts.sort(key=lambda part: -part[0])
_PATTERN = re.compile("|".join(alt for _, alt in _parts), re.IGNORECASE)
_EXACT_PATTERN = re.compile("|".join(
    r"(?<!\w)" + re.escape(p) + r"(?!\w)" for p in _EXACT_DELETIONS))

del _phrase, _repl, _word_keys, _parts


def _sub(match):
    text = match.group(0)
    repl, cased = _entries[text.lower()]
    if cased and text[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def apply_replacements(text):
    """Apply all abbreviation replacements in a single pass."""
    text = _PATTERN.sub(_sub, text)
    return _EXACT_PATTERN.sub("", text)


# Per-line cleanup ------------------------------------------------------------
_SPACES = re.compile(r"[ \t]{2,}")
_PERIOD_BEFORE_CLOSER = re.compile(r"\.(?=[\"'\)\]\}*_]+$)")


def _capitalize_line(line):
    """Uppercase the first letter, unless the line leads with a number."""
    for i, ch in enumerate(line):
        if ch.isalpha():
            return line[:i] + ch.upper() + line[i + 1:]
        if ch.isdigit():
            return line
    return line


def _delete_period_line(line):
    """Drop a terminal period, including one before closing quotes/parens."""
    s = _PERIOD_BEFORE_CLOSER.sub("", line.rstrip())
    return s[:-1] if s.endswith(".") else s


def _delete_backslash_line(line):
    """Drop a terminal backslash."""
    s = line.rstrip()
    return s[:-1] if s.endswith("\\") else s


def _format_line(line):
    indent = line[: len(line) - len(line.lstrip(" \t"))]
    if indent == " ":
        # Single leading space is deletion residue, not indentation.
        indent = ""
    body = _SPACES.sub(" ", line[len(indent):].strip())
    body = _delete_backslash_line(_delete_period_line(_capitalize_line(body)))
    return indent + body


def _format_text(text):
    return "\n".join(_format_line(line) for line in text.split("\n"))


def capitalize_first_word(text):
    """Capitalize the first letter of each line, skipping leading formatting."""
    return "\n".join(_capitalize_line(line) for line in text.split("\n"))


def delete_periods(text):
    """Delete periods that end a line, including before closing quotes."""
    return "\n".join(_delete_period_line(line) for line in text.split("\n"))


def delete_trailing_backslashes(text):
    """Delete backslashes that end a line."""
    return "\n".join(_delete_backslash_line(line) for line in text.split("\n"))


def outline_text(text):
    """Compress verbose notes into compact outline form."""
    return _format_text(apply_replacements(text))



def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Abbreviate law school notes into compact outline form."
    )
    parser.add_argument(
        "--input",
        default="input_text.txt",
        help="Input file path (default: input_text.txt)",
    )
    parser.add_argument(
        "--output",
        default="output_text.txt",
        help="Output file path (default: output_text.txt)",
    )
    args = parser.parse_args(argv)

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Error: input file '{args.input}' not found.")
        raise SystemExit(1)

    output_text = outline_text(input_text)

    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
    except OSError as e:
        print(f"Error: could not write '{args.output}': {e}")
        raise SystemExit(1)

    print(f"Processing complete! Output written to {args.output}")


if __name__ == "__main__":
    main()
