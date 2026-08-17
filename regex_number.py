import re

text = "My phone number is 555-555-5555 and my friend's number is 555-555-5556"
matches = re.findall(r"\d{3}-\d{3}-\d{4}", text) 
print(matches)

# \d matches any digits
# {3} means "exactly three of the preceding character"
# - is just a literal - that we want to match

print()
print("Regex for Text Between Parentheses")

text = "I have a (cat) and a (dog)"
matches = re.findall(r"\((.*?)\)", text)
print(matches)

# \( and \) are scaped parentheses that we want to match

# ( and ) is a capture group, meaning it groups the matched text, allowing us to reference or extract it separately.

# .*? matches any number of characters (except for line terminators) between the parentheses


print()
print("Regex for emails Multiple Capture Groups")

text = "My email is lane@example.com and my friend's email is hunter@example.com"
matches = re.findall(r"(\w+)@(\w+\.\w+)", text)
print(matches)

# \w matches any word character (alphanumeric characters and underscores)

# + means "one or more of the preceding character"

# @ is just a literal @ symbol that we want to match 

# \. is a literal . that we want to match (the . is a special character in regex, so we scape it with a leading backslash)

print()
print("Negative Lookbehind")
text = "The word cat appears here, but not in concat"
matches = re.findall(r"(?<!con)cat", text)
print(matches)