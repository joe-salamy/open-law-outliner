import argparse

# ---------------------------------------------------------------------------
# Replacement pairs, applied in order. Add your own abbreviations here.
# ---------------------------------------------------------------------------
REPLACEMENTS = [
    # Legal terms ===========================================================
    ("Plaintiffs", "P's"),
    ("plaintiffs", "P's"),
    ("Plaintiff's", "P's"),
    ("plaintiff's", "P's"),
    ("Plaintiff", "P"),
    ("plaintiff", "P"),
    ("Defendant's", "D's"),
    ("defendant's", "D's"),
    ("Defendants", "D's"),
    ("defendants", "D's"),
    ("Defendant", "D"),
    ("defendant", "D"),
    ("Hypothetical ", "Hypo "),
    ("*Hypothetical*", "*Hypo*"),
    ("Hypothetical:", "Hypo:"),
    ("hypothetical ", "hypo "),
    ("*hypothetical*", "*hypo*"),
    ("hypothetical:", "hypo:"),
    ("Personal jurisdiction", "PJ"),
    ("personal jurisdiction", "PJ"),
    ("Subject matter jurisdiction", "SMJ"),
    ("subject matter jurisdiction", "SMJ"),
    ("Jurisdiction", "Jdx"),
    ("jurisdiction", "jdx"),
    ("Jurisdictions", "Jdx's"),
    ("jurisdictions", "jdx's"),
    ("Jdxal", "Jurisdictional"),
    ("jdxal", "jurisdictional"),
    ("Summary judgment", "SJ"),
    ("summary judgment", "SJ"),
    ("Supreme Court", "SCOTUS"),
    ("Section ", "§ "),
    ("section ", "§ "),
    ("1st Amendment", "1A"),
    ("First Amendment", "1A"),
    ("2nd Amendment", "2A"),
    ("Second Amendment", "2A"),
    ("3rd Amendment", "3A"),
    ("Third Amendment", "3A"),
    ("4th Amendment", "4A"),
    ("Fourth Amendment", "4A"),
    ("5th Amendment", "5A"),
    ("Fifth Amendment", "5A"),
    ("6th Amendment", "6A"),
    ("Sixth Amendment", "6A"),
    ("7th Amendment", "7A"),
    ("Seventh Amendment", "7A"),
    ("8th Amendment", "8A"),
    ("Eighth Amendment", "8A"),
    ("9th Amendment", "9A"),
    ("Ninth Amendment", "9A"),
    ("10th Amendment", "10A"),
    ("Tenth Amendment", "10A"),
    ("11th Amendment", "11A"),
    ("Eleventh Amendment", "11A"),
    ("12th Amendment", "12A"),
    ("Twelfth Amendment", "12A"),
    ("13th Amendment", "13A"),
    ("Thirteenth Amendment", "13A"),
    ("14th Amendment", "14A"),
    ("Fourteenth Amendment", "14A"),
    ("15th Amendment", "15A"),
    ("Fifteenth Amendment", "15A"),
    ("16th Amendment", "16A"),
    ("Sixteenth Amendment", "16A"),
    ("17th Amendment", "17A"),
    ("Seventeenth Amendment", "17A"),
    ("18th Amendment", "18A"),
    ("Eighteenth Amendment", "18A"),
    ("19th Amendment", "19A"),
    ("Nineteenth Amendment", "19A"),
    ("Due process", "DP"),
    ("due process", "DP"),
    ("Default judgment", "DJ"),
    ("default judgment", "DJ"),
    ("Corporation", "Corp"),
    ("corporation", "corp"),
    ("Constitutional", "Const"),
    ("constitutional", "const"),
    ("Constitution", "Const"),
    ("constitution", "const"),
    ("constity", "constitutionality"),
    ("Articles of Confederation", "AoC"),
    ("Administration", "Admin"),
    ("administration", "admin"),
    ("Administrative", "Admin"),
    ("administrative", "admin"),
    ("President", "Pres"),
    ("president", "pres"),
    ("Presial", "Presidential"),
    ("presial", "presidential"),
    ("Secretary", "Sec"),
    ("secretary", "sec"),
    ("Executive", "Exec"),
    ("executive", "exec"),
    ("Legislative", "Legis"),
    ("legislative", "legis"),
    ("Judicial", "Judic"),
    ("judicial", "judic"),
    ("Legislature", "Legis"),
    ("legislature", "legis"),
    ("Landlords", "LL's"),
    ("landlords", "LL's"),
    ("Landlord's", "LL's"),
    ("landlord's", "LL's"),
    ("Landlord", "LL"),
    ("landlord", "LL"),
    ("Tenants", "T's"),
    ("tenants", "T's"),
    ("Tenant's", "T's"),
    ("tenant's", "T's"),
    ("Tenant", "T"),
    ("tenant", "T"),
    ("Contract ", "K "),
    ("contract ", "k "),
    (" Federal ", " Fed "),
    (" federal ", " fed "),
    (" Citizenship ", " C-ship "),
    (" citizenship ", " c-ship "),
    (" Argument ", " Arg "),
    (" argument ", " arg "),
    ("Adverse possession", "AP"),
    ("adverse possession", "AP"),
    ("Intellectual Property", "IP"),
    ("Intellectual property", "IP"),
    ("intellectual property", "IP"),
    # States ================================================================
    ("United States", "US"),
    ("Alabama", "AL"),
    ("Alaska", "AK"),
    ("Arizona", "AZ"),
    ("Arkansas", "AR"),
    ("California", "CA"),
    ("Colorado", "CO"),
    ("Connecticut", "CT"),
    ("Delaware", "DE"),
    ("Florida", "FL"),
    ("Georgia", "GA"),
    ("Hawaii", "HI"),
    ("Idaho", "ID"),
    ("Illinois", "IL"),
    ("Indiana", "IN"),
    ("Iowa", "IA"),
    ("Kansas", "KS"),
    ("Kentucky", "KY"),
    ("Louisiana", "LA"),
    ("Maine", "ME"),
    ("Maryland", "MD"),
    ("Massachusetts", "MA"),
    ("Michigan", "MI"),
    ("Minnesota", "MN"),
    ("Mississippi", "MS"),
    ("Missouri", "MO"),
    ("Montana", "MT"),
    ("Nebraska", "NE"),
    ("Nevada", "NV"),
    ("New Hampshire", "NH"),
    ("New Jersey", "NJ"),
    ("New Mexico", "NM"),
    ("New York", "NY"),
    ("North Carolina", "NC"),
    ("North Dakota", "ND"),
    ("Ohio", "OH"),
    ("Oklahoma", "OK"),
    ("Oregon", "OR"),
    ("Pennsylvania", "PA"),
    ("Rhode Island", "RI"),
    ("South Carolina", "SC"),
    ("South Dakota", "SD"),
    ("Tennessee", "TN"),
    ("Texas", "TX"),
    ("Utah", "UT"),
    ("Vermont", "VT"),
    ("Virginia", "VA"),
    ("Washington", "WA"),
    ("West Virginia", "WV"),
    ("Wisconsin", "WI"),
    ("Wyoming", "WY"),
    # Common replacements ===================================================
    ("Because", "Bc"),
    ("because", "bc"),
    (" And ", " + "),
    (" and ", " + "),
    ("Information", "Info"),
    ("information", "info"),
    (" With ", " W/ "),
    (" with ", " w/ "),
    (" Without ", " W/o "),
    (" without ", " w/o "),
    ("Professor", "Prof"),
    ("professor", "prof"),
    ("Government", "Govt"),
    ("government", "govt"),
    ("Introduction", "Intro"),
    ("introduction", "intro"),
    ("People", "Ppl"),
    ("people", "ppl"),
    (r"\-\>", "→"),
    (r"\<-", "←"),
    ("Automatically", "Auto"),
    ("automatically", "auto"),
    ("Conversation", "Convo"),
    ("conversation", "convo"),
    ("Combination", "Combo"),
    ("combination", "combo"),
    ("More than ", "> "),
    ("more than ", "> "),
    ("Less than ", "< "),
    ("less than ", "< "),
    ("Technology", "Tech"),
    ("technology", "tech"),
    ("Apartment", "Apt"),
    ("apartment", "apt"),
    (" Number ", " # "),
    (" number ", " # "),
    (" Graduate ", " Grad "),
    (" graduate ", " grad "),
    (" Regarding ", " Re. "),
    (" regarding ", " re. "),
    (" Especially ", " Esp. "),
    (" especially ", " esp. "),
    (" Professional ", " Prof. "),
    (" professional ", " prof. "),
    (" Education ", " Edu "),
    (" education ", " edu "),
    (" University ", " Uni "),
    (" university ", " uni "),
    (" Universities ", " Uni's "),
    (" universities ", " uni's "),
    (" Legitimate ", " Legit "),
    (" legitimate ", " legit "),
    # Abbreviations =========================================================
    (" Would have ", " Would've "),
    (" would have ", " would've "),
    (" Should have ", " Should've "),
    (" should have ", " should've "),
    (" Could have ", " Could've "),
    (" could have ", " could've "),
    (" Might have ", " Might've "),
    (" might have ", " might've "),
    (" Does not ", " Doesn't "),
    (" does not ", " doesn't "),
    (" Do not ", " Don't "),
    (" do not ", " don't "),
    (" Will not ", " Won't "),
    (" will not ", " won't "),
    (" Could not ", " Couldn't "),
    (" could not ", " couldn't "),
    (" Would not ", " Wouldn't "),
    (" would not ", " wouldn't "),
    (" Should not ", " Shouldn't "),
    (" should not ", " shouldn't "),
    (" Have not ", " Haven't "),
    (" have not ", " haven't "),
    (" Cannot ", " Can't "),
    (" cannot ", " can't "),
    (" Did not ", " Didn't "),
    (" did not ", " didn't "),
    # Numbers ===============================================================
    (" One ", " 1 "),
    (" one ", " 1 "),
    (" Two ", " 2 "),
    (" two ", " 2 "),
    (" Three ", " 3 "),
    (" three ", " 3 "),
    (" Four ", " 4 "),
    (" four ", " 4 "),
    (" Five ", " 5 "),
    (" five ", " 5 "),
    (" Six ", " 6 "),
    (" six ", " 6 "),
    (" Seven ", " 7 "),
    (" seven ", " 7 "),
    (" Eight ", " 8 "),
    (" eight ", " 8 "),
    (" Nine ", " 9 "),
    (" nine ", " 9 "),
    (" Ten ", " 10 "),
    (" ten ", " 10 "),
    (" First ", " 1st "),
    (" first ", " 1st "),
    (" Second ", " 2nd "),
    (" second ", " 2nd "),
    (" Third ", " 3rd "),
    (" third ", " 3rd "),
    (" Fourth ", " 4th "),
    (" fourth ", " 4th "),
    (" Fifth ", " 5th "),
    (" fifth ", " 5th "),
    (" Sixth ", " 6th "),
    (" sixth ", " 6th "),
    (" Seventh ", " 7th "),
    (" seventh ", " 7th "),
    (" Eighth ", " 8th "),
    (" eighth ", " 8th "),
    (" Ninth ", " 9th "),
    (" ninth ", " 9th "),
    (" Tenth ", " 10th "),
    (" tenth ", " 10th "),
    (" Percentage ", " % "),
    (" percentage ", " % "),
    (" Percent ", " % "),
    (" percent ", " % "),
    (",000,000", "M"),
    (",000", "K"),
    # Deletions =============================================================
    (" The ", " "),
    (" the ", " "),
    (" a ", " "),
    (" An ", " "),
    (" an ", " "),
    (" It ", " "),
    (" it ", " "),
    (" It's ", " "),
    (" it's ", " "),
    (" is ", " "),
    (" are ", " "),
    (" was ", " "),
    (" were ", " "),
    (" his ", " "),
    (" hers ", " "),
    (" their ", " "),
    (" theirs ", " "),
    ("Case Example: ", ""),
]


def apply_replacements(text):
    """Apply all abbreviation replacements to text."""
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def capitalize_first_word(text):
    """
    Capitalize the first actual character on each line, skipping formatting characters like **, quotes, and whitespace.
    Do not capitalize if the first actual character is a number.
    """
    lines = text.split("\n")
    capitalized_lines = []

    for line in lines:
        # Find the first alphanumeric character
        first_alnum_index = -1
        for i, char in enumerate(line):
            if char.isalnum():
                first_alnum_index = i
                break

        if first_alnum_index != -1 and line[first_alnum_index].isdigit():
            # Don't capitalize if first alphanumeric character is a digit
            capitalized_lines.append(line)
        else:
            # Find the first alphabetic character and capitalize it
            for i, char in enumerate(line):
                if char.isalpha():
                    line = line[:i] + char.upper() + line[i + 1 :]
                    break
            capitalized_lines.append(line)

    return "\n".join(capitalized_lines)


def delete_periods(text):
    """
    Delete periods if they are the last non-space character in a line,
    or if a line ends with ." (period before closing quote).
    """
    lines = text.split("\n")
    result_lines = []

    for line in lines:
        # Find the last non-space character
        stripped = line.rstrip()
        if stripped and stripped[-1] == ".":
            # Remove the trailing period
            line = stripped[:-1] + line[len(stripped) :]
        elif stripped and stripped.endswith('."'):
            # Remove the period before closing quote
            line = stripped[:-2] + '"' + line[len(stripped) :]
        result_lines.append(line)

    return "\n".join(result_lines)


def delete_trailing_backslashes(text):
    """
    Delete backslashes if they are the last non-space character in a line.
    """
    lines = text.split("\n")
    result_lines = []

    for line in lines:
        # Find the last non-space character
        stripped = line.rstrip()
        if stripped and stripped[-1] == "\\":
            # Remove the backslash
            line = stripped[:-1] + line[len(stripped) :]
        result_lines.append(line)

    return "\n".join(result_lines)


if __name__ == "__main__":
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
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Error: input file '{args.input}' not found.")
        raise SystemExit(1)

    output_text = apply_replacements(input_text)
    output_text = capitalize_first_word(output_text)
    output_text = delete_periods(output_text)
    output_text = delete_trailing_backslashes(output_text)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"Processing complete! Output written to {args.output}")
