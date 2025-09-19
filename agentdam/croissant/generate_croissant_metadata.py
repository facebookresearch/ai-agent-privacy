# Copyright (c) Meta Platforms, Inc. and affiliates.
import mlcroissant as mlc
import json

distribution = [
    mlc.FileObject(
        id="github-repository",
        name="github-repository",
        description="AgentDAM repository on GitHub.",
        content_url="https://github.com/facebookresearch/ai-agent-privacy",
        encoding_formats=["git+https"],
        sha256="main",
    ),
    # Within that repository, a FileSet lists all JSONL files:
    mlc.FileSet(
        id="jsonl-files",
        name="jsonl-files",
        description="JSONL files are hosted on the GitHub repository.",
        contained_in=["github-repository"],
        encoding_formats=["application/jsonlines"],
        includes="agentdam/data/wa_format/extra/*.jsonl",
    ),
]

record_sets = [
    # RecordSets contains records in the dataset.
    mlc.RecordSet(
        id="jsonl",
        name="jsonl",
        # Each record has one or many fields...
        fields=[
            # Fields can be extracted from the FileObjects/FileSets.
            # mlc.Field(
            #     id="jsonl/task_id",
            #     name="task_id",
            #     description="task_id",
            #     data_types=mlc.DataType.INT32,
            #     source=mlc.Source(
            #         file_set="jsonl-files",
            #         # Extract the field from the column of a FileObject/FileSet:
            #         extract=mlc.Extract(column="task_id"),
            #     ),
            # ),
            mlc.Field(
                id="jsonl/UID",
                name="UID",
                description="UID used to evaluate agent's final output",
                data_types=mlc.DataType.TEXT,
                source=mlc.Source(
                    file_set="jsonl-files",
                    # Extract the field from the column of a FileObject/FileSet:
                    extract=mlc.Extract(column="UID"),
                ),
            ),
            mlc.Field(
                id="jsonl/start_url",
                name="start_url",
                description="start_url, __XSITE__ needss to be replaced with env variable.",
                data_types=mlc.DataType.TEXT,
                source=mlc.Source(
                    file_set="jsonl-files",
                    # Extract the field from the column of a FileObject/FileSet:
                    extract=mlc.Extract(column="start_url"),
                ),
            ),
            mlc.Field(
                id="jsonl/intent_type",
                name="intent_type",
                description="Task type",
                data_types=mlc.DataType.TEXT,
                source=mlc.Source(
                    file_set="jsonl-files",
                    # Extract the field from the column of a FileObject/FileSet:
                    extract=mlc.Extract(column="intent_type"),
                ),
            ),
            mlc.Field(
                id="jsonl/intent_template",
                name="intent_template",
                description="user_instruction, i.e. instruction from user to an agent.",
                data_types=mlc.DataType.TEXT,
                source=mlc.Source(
                    file_set="jsonl-files",
                    extract=mlc.Extract(column="intent_template"),
                ),
            ),
            mlc.Field(
                id="jsonl/intent_data",
                name="intent_data",
                description="user_data, i.e. data that accompanies user_instruction.",
                data_types=mlc.DataType.TEXT,
                source=mlc.Source(
                    file_set="jsonl-files",
                    extract=mlc.Extract(column="intent_data"),
                ),
            ),
            mlc.Field(
                id="jsonl/plot",
                name="plot",
                description="plot -- seed used to generate user_data.",
                data_types=mlc.DataType.TEXT,
                source=mlc.Source(
                    file_set="jsonl-files",
                    extract=mlc.Extract(column="plot"),
                ),
            ),
            mlc.Field(
                id="jsonl/sensitive_data",
                name="sensitive_data",
                description="sensitive_data -- ground truth, "
                            "i.e. irrelevant piece of private data that should NOT be shared. "
                            "It needs to be converted into list of str before processing",
                data_types=mlc.DataType.TEXT,
                source=mlc.Source(
                    file_set="jsonl-files",
                    extract=mlc.Extract(column="sensitive_data"),
                ),
            ),
            # mlc.Field(
            #     id="jsonl/eval",
            #     name="eval",
            #     description="eval -- evaluation workflow, needs to be converted into valid json dict.",
            #     data_types=mlc.DataType.TEXT,
            #     source=mlc.Source(
            #         file_set="jsonl-files",
            #         extract=mlc.Extract(column="eval"),
            #     ),
            # ),
        ],
    )
]

# Metadata contains information about the dataset.
metadata = mlc.Metadata(
    name="AgentDAM",
    # Descriptions can contain plain text or markdown.
    description=(
        "We develop this benchmark to assess the ability of AI agents to satisfy data minimization, "
        "a crucial principle in preventing inadvertent privacy leakage."
    ),
    cite_as=(
        "@misc{zharmagambetov2025agentdam,"
        "title={{AgentDAM}: Privacy Leakage Evaluation for Autonomous Web Agents},"
        "author={Arman Zharmagambetov and Chuan Guo and Ivan Evtimov and Maya Pavlova and Ruslan Salakhutdinov and Kamalika Chaudhuri},"
        "year={2025},eprint={2503.09780},archivePrefix={arXiv},primaryClass={cs.AI},url={https://arxiv.org/abs/2503.09780},}"
    ),
    url="https://github.com/facebookresearch/ai-agent-privacy",
    distribution=distribution,
    record_sets=record_sets,
)

# print(metadata.issues.report())

with open("croissant_metadata.json", "w") as f:
    content = metadata.to_json()
    content = json.dumps(content, indent=2)
    # print(content)
    f.write(content)
    f.write("\n")  # Terminate file with newline

dataset = mlc.Dataset(jsonld="croissant_metadata.json")

records = dataset.records(record_set="jsonl")
# print(len(records))
for i, record in enumerate(records):
    print(record)
    if i > 10:
        break
