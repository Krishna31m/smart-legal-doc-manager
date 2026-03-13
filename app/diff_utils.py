import difflib

def compare_versions(text1, text2):

    diff = difflib.unified_diff(
        text1.splitlines(),
        text2.splitlines(),
        fromfile="before",
        tofile="after",
        lineterm=""
    )

    return "\n".join(diff)