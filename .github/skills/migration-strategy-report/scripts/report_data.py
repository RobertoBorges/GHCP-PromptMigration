"""Validate classified report records and compute separate per-pillar summaries."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys


PILLARS = ("applications", "databases", "infrastructure")
OWNERS = ("Microsoft", "Partner", "Unknown", "No Migration Needed")
STRATEGIES = ("Retire", "Retain", "Replace", "Refactor", "Replatform", "Rehost")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value, location):
    require(isinstance(value, str) and bool(value.strip()),
            "{} must be a nonempty string".format(location))
    require(not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", value),
            "{} contains unsupported control characters".format(location))


def evidence(value, location):
    require(isinstance(value, list) and bool(value),
            "{} must contain source references".format(location))
    for index, source in enumerate(value):
        text(source, "{}[{}]".format(location, index))


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON object key")
        result[key] = value
    return result


def load_model(path):
    with Path(path).open(encoding="utf-8-sig") as source:
        model = json.load(source, object_pairs_hook=unique_object)
    return model


def validate_model(model):
    require(isinstance(model, dict), "Report data must be a JSON object")
    require(model.get("schema_version") == "1.0", "schema_version must be 1.0")
    text(model.get("customer"), "customer")
    text(model.get("language"), "language")
    mode = model.get("strategy_mode", "6R")
    require(mode in ("6R", "8R"), "strategy_mode must be 6R or 8R")
    strategies = STRATEGIES + (("Rearchitect", "Rebuild") if mode == "8R" else ())
    records = model.get("records")
    require(isinstance(records, list), "records must be an array")
    index = {}
    for number, record in enumerate(records):
        location = "records[{}]".format(number)
        require(isinstance(record, dict), "{} must be an object".format(location))
        pillar = record.get("pillar")
        require(pillar in PILLARS, "{} has an invalid pillar".format(location))
        for field in ("id", "name", "rule", "rationale"):
            text(record.get(field), "{}.{}".format(location, field))
        identifier = record["id"]
        require(identifier == identifier.strip(), "{}.id has surrounding whitespace".format(location))
        key = (pillar, identifier)
        require(key not in index, "{} duplicates a pillar/id".format(location))
        index[key] = record
        for field in ("in_scope", "migration_required"):
            require(type(record.get(field)) is bool,
                    "{}.{} must be a JSON boolean".format(location, field))
        owner = record.get("ownership")
        require(owner in OWNERS, "{} has an invalid ownership".format(location))
        require(pillar == "applications" or owner != "No Migration Needed",
                "{} uses an application-only ownership".format(location))
        require(record.get("confidence") in ("High", "Medium", "Low"),
                "{} has an invalid confidence".format(location))
        evidence(record.get("evidence"), "{}.evidence".format(location))
        if pillar == "applications" and record["in_scope"]:
            require(record.get("strategy") in strategies,
                    "{} needs a valid in-scope application strategy".format(location))
        if owner == "No Migration Needed" or record.get("strategy") in ("Retain", "Retire"):
            require(not record["migration_required"],
                    "{} cannot require migration for its disposition".format(location))
        if "target" in record:
            text(record["target"], "{}.target".format(location))

    for number, record in enumerate(records):
        hosts = record.get("host_ids", [])
        require(isinstance(hosts, list), "records[{}].host_ids must be an array".format(number))
        seen = set()
        for host in hosts:
            text(host, "host_ids entry")
            require(host not in seen, "Duplicate host mapping")
            require(("infrastructure", host) in index, "Host mapping references an unknown VM/server")
            seen.add(host)

    assigned = set()
    waves = model.get("waves", [])
    require(isinstance(waves, list), "waves must be an array")
    wave_ids = set()
    for number, wave in enumerate(waves):
        location = "waves[{}]".format(number)
        require(isinstance(wave, dict), "{} must be an object".format(location))
        for field in ("id", "name"):
            text(wave.get(field), "{}.{}".format(location, field))
        require(wave["id"] not in wave_ids, "Duplicate wave ID")
        wave_ids.add(wave["id"])
        refs = wave.get("record_refs")
        require(isinstance(refs, list) and bool(refs), "{} needs record_refs".format(location))
        for ref in refs:
            require(isinstance(ref, dict), "Wave record reference must be an object")
            text(ref.get("pillar"), "record_refs.pillar")
            text(ref.get("id"), "record_refs.id")
            key = (ref["pillar"], ref["id"])
            require(key in index, "Wave references an unknown record")
            record = index[key]
            require(record["in_scope"] and record["migration_required"],
                    "Wave references an out-of-scope or non-migrating record")
            require(key not in assigned, "Record assigned more than once across waves")
            assigned.add(key)

    for field in ("questions", "blockers"):
        items = model.get(field, [])
        require(isinstance(items, list), "{} must be an array".format(field))
        seen = set()
        for number, item in enumerate(items):
            location = "{}[{}]".format(field, number)
            require(isinstance(item, dict), "{} must be an object".format(location))
            for name in ("id", "text", "owner"):
                text(item.get(name), "{}.{}".format(location, name))
            require(item["id"] not in seen, "{} has duplicate IDs".format(field))
            seen.add(item["id"])
            evidence(item.get("evidence"), "{}.evidence".format(location))

    summary = {}
    for pillar in PILLARS:
        population = [row for row in records if row["pillar"] == pillar]
        scoped = [row for row in population if row["in_scope"]]
        counts = Counter(row["ownership"] for row in scoped)
        result = {
            "portfolio": len(population),
            "in_scope": len(scoped),
            "out_of_scope": len(population) - len(scoped),
            "ownership": {owner: counts[owner] for owner in OWNERS if counts[owner]},
            "migration_required": sum(row["migration_required"] for row in scoped),
            "unassigned_migrations": sum(
                row["migration_required"] and (pillar, row["id"]) not in assigned for row in scoped
            ),
        }
        if pillar == "applications":
            result["strategies"] = dict(Counter(row["strategy"] for row in scoped))
        summary[pillar] = result
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        summary = validate_model(load_model(args.input))
    except (OSError, ValueError) as error:
        print("Report data validation FAILED: {}".format(error), file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
