def encode(obj: dict) -> str:
    """
    Build identifier from dict
    """
    # Sort checkout fields
    fields = list(sorted(obj.keys()))
    # Build identifier
    identifier = ""
    for index, field in enumerate(fields):
        identifier += f"{field}={obj[field]}"
        if index + 1 != len(fields):
            identifier += "|"
    return identifier


def decode(identifier: str) -> dict:
    """
    Decode identifiler back into dict from str
    identifier: person identifier, encoded with identifiler.encode
    """
    pairs = identifier.split("|")
    fields = {}
    for pair in pairs:
        pair = pair.split("=")
        fields[pair[0]] = pair[1]
    return fields


def compare(identifier1: str, identifier2: str, mode: str = "light") -> bool:
    """
    Compare 2 identifiers
    Supported modes: light(compare only existing pairs in each identifiler),
                     deep(if pair is not exist in another identifier, returns false)
    """
    # Check mode
    supported_mods = ["light", "deep"]
    if mode not in supported_mods:
        raise Exception(f"Mode is not supported {mode}")

    if mode == "light":
        id1 = decode(identifier1)
        id2 = decode(identifier2)

        for k, v in id1.items():
            if id2[k] and id2[k] != v:
                return False

        return True

    if mode == "deep":
        # Identifiers are already sorted and ready for direct comparison
        return identifier1 == identifier2
